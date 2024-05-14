import os


# 数据路径
def loadbib(file):
    woslist = list()
    with open(file, "r") as f:
        key = f.readlines()[0].replace("\n", "").split("\t")[1:]
    with open(file, "r") as f:
        for line in f.readlines()[1:(len(f.readlines()) - 1)]:
            field = line.replace("\n", "").split("\t")[1:]
            woslist.append(dict(zip(key, field)))
    return (woslist)


# 读入路径
input_file_path = "/Users/popo/bigdata/pythondir/qje.txt"
woslist = loadbib(input_file_path)


def basicinfo(dict_data):
    key = ["ut", "pub_year", "so", "issn", "doi", "issue", "volume", "abstract", "title", "authors", "address", "ref"]
    basic = dict(zip(key, [dict_data["UT"], dict_data["PY"], dict_data["SO"],
                           dict_data["SN"], dict_data["DI"], dict_data["IS"],
                           dict_data["VL"], dict_data["AB"], dict_data["AF"],
                           dict_data["TI"], dict_data["C1"], dict_data["CR"]]))
    return (basic)


basicinfo(woslist[0])


class PaperInfo:
    def __init__(self):
        self.ut_char = ""
        self.pub_year = ""
        self.SO = ""
        self.issn = ""
        self.doi = ""
        self.issue = ""
        self.volume = ""
        self.abstract = ""
        self.title = ""
        self.address = []
        self.ref = ""
        self.authors = []

    # 表 1：论文基本信息
    def load_basic(self, data_dict):
        self.ut_char = data_dict["UT"]
        self.pub_year = data_dict["PY"]
        self.SO = data_dict["SO"]
        self.issn = data_dict["SN"]
        self.doi = data_dict["DI"]
        self.issue = data_dict["IS"]
        self.volume = data_dict["VL"]

    # 表 2：论文摘要信息
    def load_abstract(self, data_dict):
        self.ut_char = data_dict["UT"]
        self.abstract = data_dict["AB"]

    # 表 3：论文标题信息
    def load_title(self, data_dict):
        self.ut_char = data_dict["UT"]
        self.title = data_dict["TI"]

    # 表 4：论文作者信息
    # 新分类-拆分作者姓名
    class Author:
        def __init__(self, fullname, order):
            self.fullname = fullname
            self.family_name = fullname.split(",")[0].strip() if "," in fullname else ""
            self.given_name = fullname.split(",")[1].strip() if "," in fullname else ""
            self.order = order

        def display_info(self, ut_char):
            return f"{ut_char}|{self.order}|{self.fullname}|{self.family_name}|{self.given_name}"

    def load_authors(self, data_dict):
        self.ut_char = data_dict.get("UT", "")
        author_list = data_dict.get("AF", "").split(";")
        for i, author in enumerate(author_list):
            if author:  # 如果作者名不为空
                self.authors.append(self.Author(author, i + 1))

    # 表 5：论文作者单位信息
    class Address:
        def __init__(self, affiliation, order):
            self.affiliation = affiliation
            self.order = order

        def display_info(self, ut_char):
            return f"{ut_char}|{self.order}|{self.affiliation}"

    def load_add(self, data_dict):
        self.ut_char = data_dict.get("UT", "")
        add_list = data_dict.get("C1", "").split(";")
        for i, address in enumerate(add_list):
            if address:  # 如果作者名不为空
                self.address.append(self.Address(address, i + 1))

    # 表 6：论文参考文献信息
    def load_ref(self, data_dict):
        self.ut_char = data_dict["UT"]
        self.ref = data_dict["CR"]

    # 定义输出方式
    def basic_output(self):
        return f"{self.ut_char}|{self.pub_year}|{self.SO}|{self.issn}|{self.doi}|{self.issue}|{self.volume}"

    def abstract_output(self):
        return f"{self.ut_char}|{self.abstract}"

    def title_output(self):
        return f"{self.ut_char}|{self.title}"

    def author_output(self):
        return [author.display_info(self.ut_char) for author in self.authors]

    def address_output(self):
        return [address.display_info(self.ut_char) for address in self.address]

    def ref_output(self):
        return f"{self.ut_char}|{self.ref}"

    # 定义写出文件
    def write_to_file(self, output_path, content, mode='w'):
        # 写入指定的文件
        with open(output_path, mode) as file:
            for content in content:
                file.write(content + "\n")


# 最终运行
# 输出表格 1-6

paper_basic_info = "/Users/popo/bigdata/pythondir/paper_basic_info.txt"
paper_abstract = "/Users/popo/bigdata/pythondir/paper_abstract.txt"
paper_title = "/Users/popo/bigdata/pythondir/paper_title.txt"
paper_authors = "/Users/popo/bigdata/pythondir/paper_authors.txt"
paper_address = "/Users/popo/bigdata/pythondir/paper_address.txt"
paper_reference = "/Users/popo/bigdata/pythondir/paper_reference.txt"

for data_dict in woslist:
    paper = PaperInfo()
    # 输出表 1
    paper.load_basic(data_dict)
    paper.write_to_file(paper_basic_info, paper.basic_output(), mode='a')  # 追加模式

    # 输出表 2
    paper.load_abstract(data_dict)
    paper.write_to_file(paper_abstract, paper.abstract_output(), mode='a')

    # 输出表 3
    paper.load_title(data_dict)
    paper.write_to_file(paper_title, paper.title_output(), mode='a')

    # 输出表 4
    paper.load_authors(data_dict)
    paper.write_to_file(paper_authors, paper.author_output(), mode='a')

    # 输出表 5
    paper.load_add(data_dict)
    paper.write_to_file(paper_address, paper.address_output(), mode='a')

    # 输出表 6
    paper.load_ref(data_dict)
    paper.write_to_file(paper_reference, paper.ref_output(), mode='a')
print("数据已写入输出文件。")
