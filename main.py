import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

def push_notification(title, content):
    token = os.getenv('PUSHPLUS_TOKEN')
    if not token:
        print("未配置 PUSHPLUS_TOKEN，无法推送通知")
        return
    url = f'http://www.pushplus.plus/send?token={token}&title={title}&content={content}'
    requests.get(url)

def auto_collect():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('http://www.51ns.cn/nlogin')
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
        username.send_keys(os.getenv('NS_USER'))
        password.send_keys(os.getenv('NS_PWD'))
        driver.find_element(By.CSS_SELECTOR, 'button[onclick="login()"]').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[text()="领券中心"]'))).click()
        coupons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[contains(text(), "立即领取")]')))
        
        results = []
        for coupon in coupons:
            try:
                coupon.click()
                results.append("✅ 领取成功")
            except Exception as e:
                results.append(f"❌ 领取失败：{str(e)}")
        push_notification("奈斯数码领券结果", "\n".join(results))

    except Exception as e:
        error_msg = f"错误详情：{str(e)}\n完整堆栈：{traceback.format_exc()}"
        push_notification("领券任务失败", error_msg)
    finally:
        driver.quit()

if __name__ == "__main__":
    auto_collect()
