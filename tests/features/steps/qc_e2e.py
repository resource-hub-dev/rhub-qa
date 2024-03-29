from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.qccreation_form import QCCreation_form
from steps.get_attribute import GetAttribute
from selenium.webdriver.support.ui import Select
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from behave import *
import time


@given(u'I am logged into the system with a valid user and password')
def step_impl(context):

    dt_request = GetAttribute()
    login_page = LoginPage(context)
    login_page.visit(dt_request.get_data("url"))
    login_page = LoginPage(context)
    login_page.login_btn.click()
    login_page.input(login_page.username, dt_request.get_data("username"))
    login_page.input(login_page.password, dt_request.get_data("password"))
    login_page = LoginPage(context)
    login_page.sign_in_btn.click()
    main_page = MainPage(context)
    
    time.sleep(3)
    
    qc_menu = main_page.quickcluster_btn.text

    assert(qc_menu == "QuickCluster")


@when(u'I navigate to the QuickCluster provisioning system')
def step_impl(context):
    main_page = MainPage(context)
    main_page.quickcluster_btn.click()
    time.sleep(1)
    main_page.mycluster_mn.click()
    time.sleep(3)
    main_page.newcluster_btn.click()
    time.sleep(5)

@when(u'I start the QuickCluster provisioning using default configuration')
def step_impl(context):

    dt_request = GetAttribute()
    qc_form = QCCreation_form(context)

    prd_slc = dt_request.get_data("prod_select")
    
    match prd_slc:
        case "Generic":
            qc_form.generic_rdbox.click()   #create class to select the right option based on the .json file
        case "Ceph":
            qc_form.ceph_rdbox.click()
        case "FuseKaraf":
            qc_form.fusekaraf_rdbox.click()
        case "Gluster":
            qc_form.gluster_rdbox.click()
        case "JBossEAP":
            qc_form.jbosseap_rdbox.click()
        case "OpenShift":
            qc_form.openshift_rdbox.click()
        case "OpenShift4":
            qc_form.openshift4_rdbox.click()
        case "Packstack":
            qc_form.packstack_rdbox.click()

            
    time.sleep(3)

    qc_form.qcnext_btn.click()
    time.sleep(3) 

    qc_form.regionrdu_rdbox.click()  #create class to select the right option based on the .json file
    time.sleep(2)

    qc_form.qcnext_btn.click()
    time.sleep(3)
    
    qc_form.input(qc_form.clusterid_fld, dt_request.get_data("cluster_id"))

    qc_form.baseosimage_slct.click()
    time.sleep(2)

    qc_form.qcform_body.click()

    image = Select(qc_form.baseosimage_slct)
    image.select_by_visible_text(dt_request.get_data("image_select")) 
    
    time.sleep(2)

    qc_form.qcform_body.click()

    time.sleep(2)

    qc_form.nodecount_slct.send_keys((Keys.CONTROL, "a"), dt_request.get_data("node_count"))
    
    nd_flavor = Select(qc_form.nodeflavor_slct)
    nd_flavor.select_by_value(dt_request.get_data("node_flavor"))

    qc_form.input(qc_form.aditionalhd_slct, dt_request.get_data("aditionalvhd"))
    qc_form.input(qc_form.aditionalhdsize_slct, dt_request.get_data("aditionalvhdsz"))
    
    reser_days = Select(qc_form.reservationdays_slct)
    reser_days.select_by_value(dt_request.get_data("reservationdz"))
    
    qc_form.qcnext_btn.click()

    time.sleep(4)

    yum_update = Select(qc_form.yumupdate_slct) 
    yum_update.select_by_visible_text(dt_request.get_data("yumupdate"))

    time.sleep(2)

    reg_method = Select(qc_form.registrationmethod_slct)
    reg_method.select_by_visible_text(dt_request.get_data("reg_method"))

    time.sleep(2)
    
    qc_form.qcnext_btn.click()

    time.sleep(5)

    assert qc_form.product_txt.text == dt_request.get_data("prod_select")
    assert qc_form.region_txt.text == dt_request.get_data("region_select")
    
    exp_days = dt_request.get_data("reservationdz")+" days"
    assert qc_form.reservexpiration_txt.text == exp_days

    assert dt_request.get_data("node_count") in qc_form.nodecount_txt.text
    assert qc_form.nodeflavor_txt.text == dt_request.get_data("node_flavor")
    assert qc_form.nbaddtvdk_txt.text == dt_request.get_data("aditionalvhd")
    assert qc_form.szaddtvdk_txt.text == dt_request.get_data("aditionalvhdsz")
    assert qc_form.execyumupdt_txt.text == dt_request.get_data("yumupdate")
    assert qc_form.regsrc_txt.text == dt_request.get_data("reg_method")

    qc_form.finish_btn.click()

    time.sleep(10)

@then(u'the cluster must be provisioned and available at main page')
def step_impl(context):
    dt_request = GetAttribute()
   
    cluster_name = dt_request.get_data("cluster_id")
    
    name_in_table = context.browser.find_element(By.XPATH, '/html/body/div/div/main/section/article/div[2]/table/tbody/tr[1]/td[2]/a').text
    status_in_table = context.browser.find_element(By.XPATH, '/html/body/div/div/main/section/article/div[2]/table/tbody/tr[1]/td[7]').text

    if (name_in_table != cluster_name):
    
        for i in range (1, 100, +1):
            pos_ph = str(i)
            path_table_name = context.browser.find_element(By.XPATH, '/html/body/div/div/main/section/article/div[2]/table/tbody['+pos_ph+']/tr[1]/td[2]/a')
            path_table_status = context.browser.find_element(By.XPATH, '/html/body/div/div/main/section/article/div[2]/table/tbody['+pos_ph+']/tr[1]/td[7]')

            name_in_table = path_table_name.text
            status_in_table = path_table_status.text

            if (name_in_table == cluster_name):
                break

    else:
        print ("Cluster "+cluster_name+" not found")
        assert False

    assert status_in_table == "Queued", print("The "+name_in_table+"Cluster was not provisioned or is not active. The actual status is: "+status_in_table)

    time.sleep(10)