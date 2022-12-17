import random
import time
import requests
import urllib3
from lxml import etree


# 请求页面
def fetch_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/108.0.0.0 Safari/537.36'}
    s = requests.session()
    s.keep_alive = False
    response = s.get(url, headers=headers, verify=False)
    return response


# 解析页面
def parse_page(response):
    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(response.text, parser=parser)

    with open('maoyan_top100_movies_list.txt', 'a', encoding='utf-8') as f:
        for i in range(1, 11):
            try:
                rank = tree.xpath(f'//dd[{i}]/i/text()')[0]
                name = tree.xpath(f'//dd[{i}]/div/div/div[1]/p[1]/a/text()')[0]
                actors = tree.xpath(f'//dd[{i}]/div/div/div[1]/p[2]/text()')[0]
                score = tree.xpath(f'//dd[{i}]/div/div/div[2]/p/i[1]/text()')[0] + \
                        tree.xpath(f'//dd[{i}]/div/div/div[2]/p/i[2]/text()')[0]
                date = tree.xpath(f'//dd[{i}]/div/div/div[1]/p[3]/text()')[0]
                f.write(f"名称：{name}")
                f.write("\n")
                f.write(f"评分：{score}")
                f.write("\n")
                f.write(f"排名：{rank}")
                f.write("\n")
                f.write(str(actors).strip())  # 去除字符串前后空白字符 （自带前缀：“主演：”）
                f.write("\n")
                f.write(date)  # 自带前缀：”上映时间：“
                f.write("\n")
                f.write("---------------------------")
                f.write("\n")
            except IndexError:  # 如果出现该错误，则很有可能是请求的页面被重定向到滑块验证页面，请求返回的是这个验证页面的HTML代码
                print("Error！可能被重定向到滑块验证页面，请尝试手动访问如下链接进行滑块验证：")
                print(response.url)
                print("并将验证后URL中的requestCode复制到代码中请求的URL中，删除文本文件中的内容，然后重启程序。")
                return False
            except IOError:
                print("Error: 没有找到文件或读取文件失败")
    return True


# 程序入口
if __name__ == '__main__':
    # 关闭警告
    urllib3.disable_warnings()
    # 滑块验证获取到的请求代码requestCode
    request_code = "6f9de047cbb62d62bded2865bcb9678ek59lu"
    isNormal = True

    # 翻页
    for i in range(0, 100, 10):
        print(f"正在爬取第{int((i + 10) / 10)}页电影信息......")
        url = f"https://www.maoyan.com/board/4?requestCode={request_code}&offset={str(i)}"
        response = fetch_page(url)
        isNormal = parse_page(response)
        if isNormal:
            print("完成")
        else:
            break
        time.sleep(random.randint(3, 12))  # 随机秒数延迟以模拟真人

    if isNormal:
        print("”猫眼电影TOP100榜“爬取完成！")
        print("若要检查文件请查看文件”maoyan_top100_movies_list.txt“。")
        print("唐靖")
    else:
        print("程序未完成！请尝试根据错误提示解决。")
