import heapq
import uuid
import sys
import os
import datetime
import redis
from enum import Enum
from typing import List, Tuple
from queue import Queue
from threading import Thread, Semaphore
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

sys.path[0] = os.path.abspath(os.curdir)
from digitalsmart.celeryconfig import app


class FileType(Enum):
    DOC = 1
    DOCX = 2


class PageType(Enum):
    EVERY = 1
    EVEN = 2
    SINGULAR = 3
    SPECIFIED = 4


class ConversionFile:
    redis_obj = redis.Redis(host='localhost', port=6379)

    @app.task(queue='docx')
    def pdf_parse_to_docx(self, file_path: str, uid: uuid, page_type: PageType, exchange_type: FileType, page: str):
        """
        :param file_path:需要转化的文件路径
        :param uid:缓存key
        :param page_type:转换页面类型
        :param exchange_type:转换文件类型
        :param page:需要转化的页面 ,如 1,3,4-7
        :return:
        """

        pdf_file = open(file_path, 'rb')
        file_type = None  # 转化的类型
        if exchange_type == FileType.DOC:
            file_type = "doc"
        if exchange_type == FileType.DOCX:
            file_type = "docx"
        # page_list需要转化的页面
        judge_pagetype, page_list = ConversionFile.anlayse_which_page_need_exchange(page,
                                                                                    page_type)
        # 准备写入文件
        write_path = "./media/pdf/" + str(uid) + "." + file_type
        write_file = open(write_path, mode="a+", encoding='utf-8')
        ConversionFile.exchange_file_type(pdf_file, write_file, judge_pagetype, page_list)
        write_file.close()
        pdf_file.close()
        ConversionFile.redis_obj.set(str(uid), 1)  # 将转化状态写入内存，用户再次请求相同文件时直接取文件，不用再转换一边
        ConversionFile.redis_obj.expire(str(uid), datetime.timedelta(days=1))

    @staticmethod
    def anlayse_which_page_need_exchange(page: str, page_type: PageType) -> Tuple[PageType, List[int]]:
        """
        :param page:
        :param page_type:
        :return:
        """
        # 存放需要指定解析的页码
        page_list = list()
        # 用来判断是用户想要哪种页面转换类型，1表示转换所有页，2表示偶数，3偶数页，4表示特定页码
        judge_pagetype = PageType.EVERY
        if page_type == PageType.EVERY:
            judge_pagetype = PageType.EVERY
        if page_type == PageType.EVEN:
            judge_pagetype = PageType.EVEN
        if page_type == PageType.SINGULAR:
            judge_pagetype = PageType.SINGULAR

        if page_type == PageType.SPECIFIED:
            judge_pagetype = PageType.SPECIFIED
            page_set = page.split(",")
            for page in page_set:
                try:
                    page = int(page)  # 针对单独一个页面，要是报错说明需要解析的页面集合是这种类型1,2,3-8这类类型的
                    page_list.append(page)
                except ValueError:
                    # 解析的页面集合是这种类型1,2,3-8这类类型的
                    page_range = page.split("-")
                    if len(page_range) == 2:
                        try:
                            start_page = int(page_range[0])
                            end_page = int(page_range[1])
                            # 都是数字的情况下继续
                            # 起始必须小于等于结束页
                            if start_page <= end_page:
                                for page in range(start_page, end_page + 1):  # 右闭
                                    page = int(page)
                                    page_list.append(page)
                        except ValueError:
                            judge_pagetype = PageType.EVERY
        return judge_pagetype, page_list

    @staticmethod
    def exchange_file_type(pdf_file, write_file, judge_pagetype: PageType, page_list):
        parser = PDFParser(pdf_file)
        doc = PDFDocument()  # 创建一个PDF文档
        parser.set_document(doc)  # 连接分析器 与文档对象
        doc.set_parser(parser)
        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()
        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()  # 创建PDf 资源管理器 来管理共享资源
            laparams = LAParams()  # 创建一个PDF设备对象
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)  # 创建一个PDF解释器对象
            count = 0  # 计算第几页
            task_queue = Queue()  # 线程锁--用来记录有多少线程开启，等待所有线程结束后在写入文件
            lock = Semaphore(1)  # 保证数据不差错
            task_lock = Semaphore(5)  # 控制线程个数
            layout_list = []  # 用于并发时存放解析出来的layout，用优先队列来保证解析成功后写入文件时顺序不会乱
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                def fast(page_index, page_content):  # page_index指第几页，page_content页面内容，
                    if judge_pagetype == PageType.EVERY:
                        pass
                    if judge_pagetype == PageType.EVEN:
                        if page_index % 2 != 0:
                            task_queue.put(1)
                            task_lock.release()
                            return
                    if judge_pagetype == PageType.SINGULAR:
                        if page_index % 2 == 0:
                            task_queue.put(1)
                            task_lock.release()
                            return
                    if judge_pagetype == PageType.SPECIFIED:
                        if len(page_list) == 0:
                            task_queue.put(1)
                            task_lock.release()

                            return
                        if page_index not in page_list:
                            task_queue.put(1)
                            task_lock.release()

                            return
                        # 页面所在列表的索引
                        element_index = page_list.index(page_index)
                        # 将解析了的页面索引pop掉，从而在列表长度为0时可以自动break结束
                        page_list.pop(element_index)
                    # 加锁保证数据正确
                    lock.acquire()
                    interpreter.process_page(page_content)
                    layout = device.get_result()
                    lock.release()
                    heapq.heappush(layout_list, (page_index, layout))  # 设置优先级,页码数作为优先级，越小越优先
                    task_queue.put(1)
                    task_lock.release()

                count += 1  # 这个表示第几页，同时也可表示有多少线程
                # 接受该页面的LTPage对象
                Thread(target=fast, args=(count, page)).start()
                task_lock.acquire(timeout=5)
            # 用来统计线程完成的个数
            num = 0
            while 1:
                task_queue.get()
                num += 1
                if count == num:  # 线程都完成了
                    break
            #  同步写入文件
            while layout_list:
                # 根据页码数大小从小到大取出内容写入文件中
                layout_tuple = heapq.heappop(layout_list)
                for x in layout_tuple[1]:
                    if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
                        # 保存文本内容
                        results = x.get_text()
                        write_file.write(results + '\n')
        parser.close()


if __name__ == "__main__":
    pdf_filepath, redis_key, page_type, to_file_type, need_conversion_page = sys.argv[1:6]
    if page_type == "PageType.EVERY":
        page_type = PageType.EVERY
    elif page_type == "PageType.EVEN":
        page_type = PageType.EVEN
    elif page_type == "PageType.SINGULAR":
        page_type = PageType.SINGULAR
    elif page_type == "PageType.SPECIFIED":
        page_type = PageType.SPECIFIED

    if to_file_type == "FileType.DOCX":
        to_file_type = FileType.DOCX
    elif to_file_type == "FileType.DOC":
        to_file_type = FileType.DOC
    conversion_file = ConversionFile()
    conversion_file.pdf_parse_to_docx(conversion_file, pdf_filepath, redis_key, page_type, to_file_type,
                                      need_conversion_page)
