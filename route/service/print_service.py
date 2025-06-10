import cups, datetime, random
from conf.conf import PRINTER_NAME
from route.service.feishu_service import SENTENCES
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
    

    @staticmethod
    def print_daily_english_study():
        """
        打印每日英语学习计划
        :param printer_name: 打印机名称
        :return:
        """
        # 需要包括标题日期和答案
        now_str = datetime.datetime.now().strftime("%Y-%m-%d")
        title = f"{now_str} 复习"
        sentences = dict()
        while len(sentences) < 20:
            random_num = random.randint(0, len(SENTENCES) - 1)
            if SENTENCES[random_num]["sentence"] not in sentences:
                sentences[SENTENCES[random_num]["sentence"]] = SENTENCES[random_num]["translation"]
        sentences = [[e, sentences[e]] for e in sentences]
        content = ""
        for i, e in enumerate(sentences):
            content += f"{i + 1}: {e[1]}<br/><br/>"
        content += "<br/>" * 3
        for i, e in enumerate(sentences):
            content += f"{i + 1}: {e[0]}<br/>"

        pdfmetrics.registerFont(TTFont('songti', 'doc/songti.ttf'))

        file_path = f"/tmp/{now_str}.pdf"

        # 创建文档
        doc = SimpleDocTemplate(file_path, 
                                pagesize=A4,
                                rightMargin=72, 
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72)

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
                "ChineseTitle",
                parent=styles["Normal"],
                fontName="songti",
                fontSize=20, # 字体大小
                leading=24, # 行间距
                alignment=1,  # 1表示居中对齐
                spaceAfter=6,    # 段落后间距
                textColor=colors.red
            )

        content_style = ParagraphStyle(
                "ChineseContent",
                parent=styles["Normal"],
                fontName="songti",
                fontSize=12, # 字体大小
                leading=16, # 行间距
                alignment=0,  # 0表示左对齐
                spaceAfter=6,    # 段落后间距
                textColor=colors.black
            )

        
        # 内容容器
        story = []

        # 添加段落
        styles = getSampleStyleSheet()
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(content, content_style))

        # 生成文档
        doc.build(story)

        PrintService.print_page(file_path)





if __name__ == "__main__":
    # PrintService.print_daily_english_study()
    pass
    # PrintService.print_page("2025-05-15.pdf")