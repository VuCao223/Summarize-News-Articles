import time
import requests
from bs4 import BeautifulSoup
import os
import re
import html
from urllib.parse import urljoin

def save_to_text_file(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write('\n'.join(content))

# Đường dẫn đến thư mục lưu các tệp văn bản
output_folder = 'document'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

url = "https://www.baodanang.vn/channel/5432/"
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

news = soup.find(class_=["newsfirst"])
news1 = soup.find(class_=["items-next"])
news2 = soup.find(class_=["list-full-1"])

printed_links = set()  # Tạo một tập hợp để lưu trữ các đường dẫn đã in

# Tạo danh sách lưu trữ nội dung từ tất cả các tệp
all_articles = []

def print_unique_link(link, idx, output_folder):
    if link not in printed_links:
        printed_links.add(link)
        html_url = requests.get(link).text
        soup_url = BeautifulSoup(html_url, 'lxml')
        content = soup_url.find(class_='col-content')
        if content:
            for tag in content.find_all('p', style=lambda value: value and 'text-align:right' in value.lower()):
                tag.decompose()

            all_p_tags = content.find_all('p')
            all_p_tags = all_p_tags[1:-1]  # Loại bỏ thẻ <p> đầu tiên và cuối cùng

            whole_article = []
            for subdiv in all_p_tags:
                p_content = " ".join(subdiv.stripped_strings)
                p_content = p_content.replace('\xa0', ' ')  # Thay thế khoảng trắng không thể nhận diện
                p_content = re.sub(r'[^\w\s,.?!]', '', p_content)  # Loại bỏ kí tự đặc biệt
                p_content = re.sub(r'\.\s+', '.\n', p_content)  # Tự xuống dòng sau dấu chấm
                p_content = p_content.lower()
                whole_article.append(html.unescape(p_content))  # Thêm nội dung đã thay thế vào danh sách

            # Ghi nội dung vào tệp văn bản trong thư mục đích
            if whole_article not in all_articles:
                all_articles.append(whole_article)

                # Determine the appropriate index
                current_index = len(all_articles) - 1
                file_name = f"article_{current_index + 1}.txt"
                file_path = os.path.join(output_folder, file_name)
                save_to_text_file(whole_article, file_path)

                print(f"Saved content from article {current_index + 1} to '{file_path}'.")
# Thu thập các liên kết trong các phần tử có class "item-first", "item", "item_first", và "item first"
for idx, parent in enumerate(news.find_all(["div"], class_=["item-first"])):
    a_tag = parent.find("a")
    if a_tag and 'href' in a_tag.attrs:
        full_link = urljoin(url, a_tag['href'])
        print_unique_link(full_link, idx, output_folder)

# Thu thập các liên kết trong các phần tử "li" có class "item" hoặc "item_first"
for idx1, parent1 in enumerate(news1.find_all(["li"], class_=["item", "item_first"])):
    b_tag = parent1.find("a")
    if b_tag and 'href' in b_tag.attrs:
        full_link = urljoin(url, b_tag['href'])
        print_unique_link(full_link, idx1, output_folder)

# Thu thập các liên kết trong các phần tử "li" có class "item first" hoặc "item"
for idx2, parent2 in enumerate(news2.find_all(["li"], class_=["item first", "item"])):
    c_tag = parent2.find("a", class_="avatar")
    if c_tag and 'href' in c_tag.attrs:
        full_link = urljoin(url, c_tag['href'])
        print_unique_link(full_link, idx2, output_folder)
all_content = []
for article in all_articles:
    all_content.extend(article)

# Save all content to a single text file
output_file_path = os.path.join(output_folder, 'all_articles.txt')
save_to_text_file(all_content, output_file_path)
print(f"Saved all content to '{output_file_path}'.")