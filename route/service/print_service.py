import cups
from conf.conf import PRINTER_NAME
class PrintService:

    @staticmethod
    def print_page(file_path):
        """
        打印文件
        :param printer_name: 打印机名称
        :param file_path: 文件路径
        :return:
        """
        conn = cups.Connection()
        job_id = conn.printFile(PRINTER_NAME, file_path, "1", {})
        return job_id