class Hander_File:
    def hander_file(self, file):
        for c in file.chunks(chunk_size=64):
            yield c