from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def push_notification(title, content):
    token = os.getenv('PUSHPLUS_TOKEN')
    url = f'http://www.pushplus.plus/send?token={token}&title={title}&content={content}'
    requests.get(url)

def auto_collect():
    options = Options()
    options.add_argument('--headless')  # 无界面模式
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        # 登录
        driver.get('http://www.51ns.cn/nlogin')
        username = driver.find_element(By.ID, 'username')
        password = driver.find_element(By.ID, 'password')
        username.send_keys(os.getenv('NS_USER'))
        password.send_keys(os.getenv('NS_PWD'))
        driver.find_element(By.ID, 'loginBtn').click()

        # 进入领券中心
        driver.find_element(By.XPATH, '//a[text()="领券中心"]').click()

        # 领取所有优惠券
        coupons = driver.find_elements(By.XPATH, '//div[contains(@class, "coupon-item")]//button[text()="立即领取"]')
        results = []
        for coupon in coupons:
            try:
                coupon.click()
                results.append("✅ 领取成功")
            except:
                results.append("❌ 领取失败")

        # 推送结果
        push_notification("领券结果", "\n".join(results))

    except Exception as e:
        push_notification("领券失败", str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    auto_collect()
