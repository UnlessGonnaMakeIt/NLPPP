import os
import time
from pydub import AudioSegment
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 配置文件或环境变量中提取EdgeDriver路径
EDGE_DRIVER_PATH = 'C:/Users/Ting/Documents/edgedriver_win64/msedgedriver.exe'

def setup_edge_driver():
    """设置Edge浏览器选项并返回WebDriver实例"""
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    edge_options.add_argument("--disable-gpu")
    service = EdgeService(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver

def get_current_url(driver):
    """获取当前标签页的URL"""
    try:
        current_url = driver.execute_script("return window.location.href")
        return current_url
    except Exception as e:
        print(f"获取当前URL时发生错误: {e}")
        return None

def recognize_speech_from_url(driver, url, language='zh-CN'):
    """从给定的URL中提取音频并进行语音识别"""
    driver.get(url)
    
    # 等待页面完全加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    
    try:
        # 等待视频元素加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'video'))
        )
        
        video_element = driver.find_element(By.TAG_NAME, 'video')
        audio_url = video_element.get_attribute('src')
        
        try:
            audio = AudioSegment.from_file(audio_url, format="mp4")
            audio.export("temp_audio.wav", format="wav")
        except Exception as e:
            print(f"处理音频时发生错误: {e}")
            return
        
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                print("Recognized Text: ", text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        
        # 确保临时文件被删除
        try:
            os.remove("temp_audio.wav")
        except Exception as e:
            print(f"删除临时文件时发生错误: {e}")
    
    except TimeoutException:
        print("Timed out waiting for video element. Please check the page.")
    
    driver.quit()

if __name__ == "__main__":
    input("请手动打开B站视频并按回车继续...")
    
    driver = setup_edge_driver()
    video_url = get_current_url(driver)
    
    if video_url:
        print(f"Detected video URL: {video_url}")
        recognize_speech_from_url(driver, video_url)
    else:
        print("未能检测到视频URL，请确保B站视频窗口处于活动状态。")
    
    driver.quit()
