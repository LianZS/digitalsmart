import heapq
import sys
import datetime
from queue import Queue

from threading import Thread, Semaphore
from digitalsmart.settings import redis_cache
from pdfminer.pdfparser import PDFParser, PDFDocument

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.converter import PDFPageAggregator

from pdfminer.layout import *

from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from datainterface.models import PDFFile


class ConversionFile:
    @staticmethod
    def pdf_parse_docx(filepath, uid, page_type, exchange_type, page):
        """

        将pdf转为doc格式

       :param filepath: 上传魏文件路径
       :param uid: 用户访问唯一标识
       :param page_type:  every---转换每一页;singular--转换奇数页;
       even--转换偶数页;specified--指定页转换,若为此选项，需要分析要转换哪些页，页码或者用逗号分隔的页码范围
       （例如：1,3-5，8,9表示要转换1,
        3,4,5,8,9）
       :param exchange_type: 转换类型有:  docx,doc
       :param page:  如1,3-5，8,9表示要转换1,3,4,5,8,9这几页
       :return:
       """

        # 存放需要指定解析的页码
        page_list = list()
        # 用来判断是用户想要哪种页面转换类型，1表示转换所有页，2表示偶数，3偶数页，4表示特定页码

        judge_pagetype = 0
        if page_type == "every":
            judge_pagetype = 1
        if page_type == "even":
            judge_pagetype = 2
        if page_type == "singular":
            judge_pagetype = 3

        if page_type == "specified":
            judge_pagetype = 4
            page_set = page.split(",")
            for page in page_set:
                try:
                    # 不是数字类型的话说明可能是3-8这类类型的
                    page = int(page)
                    page_list.append(page)
                except ValueError:
                    # "3-5类型的页面范围"
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
                            judge_pagetype = 1
        # 准备写入文件
        writepath = "./media/pdf/" + str(uid) + "." + exchange_type
        f = open(writepath, "a+")
        # fp = open(filepath, 'rb')  # 以二进制读模式打开

        # 用文件对象来创建一个pdf文档分析器
        fp = open(filepath, "rb")

        parser = PDFParser(fp)

        # 创建一个PDF文档

        doc = PDFDocument()

        # 连接分析器 与文档对象

        parser.set_document(doc)

        doc.set_parser(parser)

        # 提供初始化密码

        # 如果没有密码 就创建一个空的字符串

        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略

        if not doc.is_extractable:

            raise PDFTextExtractionNotAllowed

        else:

            # 创建PDf 资源管理器 来管理共享资源

            rsrcmgr = PDFResourceManager()

            # 创建一个PDF设备对象

            laparams = LAParams()

            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # 创建一个PDF解释器对象

            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量

            # num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

            # 循环遍历列表，每次处理一个page的内容
            count = 0  # 计算第几页
            # 线程锁--用来记录有多少线程开启，等待所有线程结束后在写入文件
            q = Queue()
            lock = Semaphore(1)
            # 用于并发时存放解析出来的layout，用优先队列来保证解析成功后写入文件时顺序不会乱
            layout_list = []
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                def fast(page_index, page_content):
                    #  page_index指第几页，page_content页面内容，

                    if judge_pagetype == 1:
                        pass
                    if judge_pagetype == 2:
                        if page_index % 2 != 0:
                            q.put(1)
                            return
                    if judge_pagetype == 3:
                        if page_index % 2 == 0:
                            q.put(1)

                            return
                    if judge_pagetype == 4:
                        if len(page_list) == 0:
                            q.put(1)

                            return
                        if page_index not in page_list:
                            q.put(1)

                            return
                        # 页面所在列表的索引
                        element_index = page_list.index(page_index)
                        # 将解析了的页面索引pop掉，从而在列表长度为0时可以自动break结束
                        page_list.pop(element_index)

                    # num_page += 1  # 页面增一
                    # 加锁保证数据正确
                    lock.acquire()
                    interpreter.process_page(page_content)
                    layout = device.get_result()
                    lock.release()
                    heapq.heappush(layout_list, (page_index, layout))  # 设置优先级,页码数作为优先级，越小越优先
                    q.put(1)

                count += 1  # 这个表示第几页，同时也可表示有多少线程
                # 接受该页面的LTPage对象
                Thread(target=fast, args=(count, page)).start()

            # 用来统计线程完成的个数
            num = 0

            while 1:
                q.get()
                num += 1
                if count == num:  # 线程都完成了
                    break
            #  同步写入文件
            while layout_list:
                # 根据页码数大小从小到大取出内容写入文件中
                layout_tuple = heapq.heappop(layout_list)
                for x in layout_tuple[1]:
                    # if isinstance(x, LTImage):  # 图片对象
                    #
                    #     num_image += 1
                    #
                    # if isinstance(x, LTCurve):  # 曲线对象
                    #
                    #     num_curve += 1
                    #
                    # if isinstance(x, LTFigure):  # figure对象
                    #
                    #     num_figure += 1
                    #
                    if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容

                        # num_TextBoxHorizontal += 1  # 水平文本框对象增一

                        # 保存文本内容

                        results = x.get_text()

                        f.write(results + '\n')

        fp.close()
        # 保存到数据库
        pdf = PDFFile()
        pdf.id = uid
        pdf.file = "pdf/" + str(uid) + "." + exchange_type
        pdf.save()
        f.close()
        redis_cache.set(str(uid), 1)  # 将转化状态写入内存，用户再次请求相同文件时直接取文件，不用再转换一边
        redis_cache.expire(filepath, time_interval=datetime.timedelta(minutes=60))


if __name__ == "__main__":
    try:
        conversion_file = ConversionFile()
        filepath, uid, page_type, exchange_type, page = sys.argv[1:4]
        conversion_file.pdf_parse_docx(filepath, uid, page_type, exchange_type, page)

    except Exception as e:
        print(sys.argv)
