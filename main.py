import traceback  # 新增导入
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
    response = requests.get(url)
    if response.status_code != 200:
        print(f"推送通知失败，状态码：{response.status_code}")

def auto_collect():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        # 登录页面
        driver.get('http://www.51ns.cn/nlogin')
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        username.send_keys(os.getenv('NS_USER'))
        password.send_keys(os.getenv('NS_PWD'))
        driver.find_element(By.CSS_SELECTOR, 'button[onclick="login()"]').click()

        # 进入领券中心
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="领券中心"]'))
        ).click()

        # 领取所有优惠券
        coupons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//button[contains(text(), "立即领取")]'))
        )
        results = []
        for coupon in coupons:
            try:
                coupon.click()
                results.append("✅ 领取成功")
            except Exception as e:
                results.append(f"❌ 领取失败：{str(e)}")

        push_notification("奈斯数码领券结果", "\n".join(results))

    except Exception as e:
        error_detail = traceback.format_exc()  # 捕获完整异常堆栈
        push_notification("领券任务失败", f"错误详情：{str(e)}\n完整堆栈：{error_detail}")
    finally:
        driver.quit()

if __name__ == "__main__":
    auto_collect()
