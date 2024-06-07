from selenium import webdriver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options
import streamlit as st
import pandas as pd
import numpy as np
import time


logging.basicConfig(filename="shopping.log",filemode="w",level=logging.DEBUG,force=True)

#web driver initialization
edge_options = Options()
edge_options.add_argument("--incognito")
edge_options.add_argument("--headless") 
edge_options.add_argument("--disable-gpu")
driver=webdriver.Edge(options=edge_options)

driver.get("https://www.amazon.in/")
logging.info("Successfully initialized")
st.title("WELCOME TO SWIFT PRODUCT PRICE FINDER 🎯🖥️")
st.info("Say goodbye to time-consuming searches and hello to swift, efficient, and reliable price discovery. Whether you're a savvy shopper or a business professional, Swift Product Price Finder revolutionizes the way you access and compare product prices, making informed decisions faster than ever before.")
#searching the website
search_box=driver.find_element("xpath",'//*[@id="twotabsearchtextbox"]')
logging.warning("Please make sure to type in the right product")
m=st.text_input("Enter the product and its specification")
if m!="":
    #m=input("Enter what you want to find\n")
    search_box.send_keys(m)
    search_button=driver.find_element("xpath",'//*[@id="nav-search-submit-button"]')
    search_button.click()
    logging.info("Successfully searched the product")

    #scrapping the information
    desc=[]
    pric=[]
    #generally xpath is in the format '//{the division}[@class={the class}]'
    phones=driver.find_elements("xpath","//span[@class='a-size-medium a-color-base a-text-normal']")
    #prices=driver.find_elements("xpath","//span[@class='a-price-whole']")
    prices=driver.find_elements("xpath","//a[@class='a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal']")

    
    for i in phones:
        desc.append(i.text)
    for j in prices:
        pric.append(j.text)

    actual_price=[]
    discount_price=[]
    print(desc)
    print(pric) 
    for j in pric:
        dis,act=j.split(':')
        actual_price.append(act)
        discount_price.append(dis)
    print(actual_price)
    print(discount_price)
    logging.info("Successfully scrapped the data")

    #constructing a dataframe
    desc1=pd.DataFrame(desc,columns=["Product Name"])
    pric1=pd.DataFrame(actual_price,columns=['M.R.P'])
    pric1['M.R.P']=pric1['M.R.P'].str.replace('\n','')
    pric2=pd.DataFrame(discount_price,columns=['Price after discount'])
    pric2['Price after discount']=pric2['Price after discount'].str.replace('M.R.P'," ")

    df1=pd.concat([desc1,pric1,pric2],axis=1)
    print(df1)
    #df1 = st.data_editor(df1, num_rows="dynamic")

    #st.dataframe(df1,use_container_width=True)
    st.table(df1)

    #making a dictionary of the description and the price
    k={}
    for i in desc:
        for j in pric:
            k[i]=[j]

    #storage of the list of items into a doc
    file=open("items.txt","w",encoding="utf-8")
    file.write(str(df1))
    file.close()
else:
    st.stop()
