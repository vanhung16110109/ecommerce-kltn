import sqlite3
#from .models import Province


def show_province():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT name FROM province")
    items = c.fetchall()
    return items
    

def show_district():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT * FROM district")
    items = c.fetchall()
    return items


def show_ward():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT * FROM ward")
    items = c.fetchall()
    return items


def show_village():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT * FROM village")
    items = c.fetchall()
    return items


def show_province_district():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT province.name, district.name FROM province, district WHERE province.provinceid = district.provinceid")
    items = c.fetchall()
    return items


def show_province_district_ward():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT province.name, district.name,ward.name FROM province, district, ward WHERE province.provinceid = district.provinceid and district.districtid = ward.districtid")
    items = c.fetchall()
    return items


def show_province_district_ward_village():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT province.name, district.name, ward.name, village.name FROM province, district, ward, village WHERE province.provinceid = district.provinceid and district.districtid = ward.districtid and ward.wardid = village.wardid")
    items = c.fetchall()
    return items


# search district in province
def show_province_district_search(provinceid):
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT province.name, district.districtid, district.name FROM province, district WHERE province.provinceid = district.provinceid and district.provinceid = (?) ", (provinceid,))
    items = c.fetchall()
    return items


# search ward in district
def show_province_district_ward_search(districtid):
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT province.name, district.name, ward.wardid, ward.name FROM province, district, ward WHERE province.provinceid = district.provinceid and district.districtid = ward.districtid and ward.districtid = (?)", (districtid,))
    items = c.fetchall()
    return items


# search village in ward
def show_province_district_ward_village(wardid):
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #query database
    c.execute("SELECT province.name, district.name, ward.name, village.villageid, village.name FROM province, district, ward, village WHERE province.provinceid = district.provinceid and district.districtid = ward.districtid and ward.wardid = village.wardid and ward.wardid = (?)", (wardid,))
    items = c.fetchall()
    return items


def search_province():
    #connect database    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    show_province()
    provinceid = input()
    show_province_district_search(provinceid)
    districtid = input()
    show_province_district_ward_search(districtid)
    wardid = input()
    show_province_district_ward_village(wardid)
    conn.close()
