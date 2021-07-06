# Generated by Django 3.1.7 on 2021-07-04 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210705_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeaddress',
            name='district',
            field=models.CharField(blank=True, choices=[('3695', 'Thành Phố Thủ Đức'), ('3694', 'Huyện Quảng Hòa'), ('3451', 'Quận Đặc Biệt'), ('3450', 'Quận Vật Tư HN'), ('3449', 'Quận Vật Tư HCM'), ('3448', 'Quận Đặc Biệt DC'), ('3447', 'Quận Đặc Biệt'), ('3446', 'Huyện Ia H Drai'), ('3445', 'Huyện Long Mỹ'), ('3444', 'Huyện Phú Riềng'), ('3443', 'Thị xã Duyên Hải'), ('3442', 'Quận Đặc Biệt'), ('3441', 'Thị xã Kỳ Anh'), ('3440', 'Quận Nam Từ Liêm'), ('3418', 'Huyện M Đrắk'), ('3329', 'Thị xã Kiến Tường'), ('3327', 'Huyện Yên Mô'), ('3323', 'Huyện Xuân Trường'), ('3320', 'Huyện Vũ Quang'), ('3319', 'Huyện Vụ Bản'), ('3317', 'Huyện Vĩnh Thạnh'), ('3315', 'Huyện Vĩnh Hưng'), ('3312', 'Huyện Vân Canh'), ('3311', 'Huyện Văn Quan'), ('3310', 'Huyện Văn Lãng'), ('3308', 'Huyện Trực Ninh'), ('3305', 'Huyện Trà Lĩnh'), ('3304', 'Huyện Trà Bồng'), ('3303', 'Huyện Thường Tín'), ('3302', 'Huyện Thuận Nam'), ('3301', 'Huyện Thuận Bắc'), ('3300', 'Huyện Thới Lai'), ('3299', 'Huyện Thông Nông'), ('3298', 'Huyện Thiệu Hóa'), ('3294', 'Huyện Thanh Miện'), ('3293', 'Huyện Thạnh Hóa'), ('3292', 'Huyện Thanh Hà'), ('3291', 'Huyện Thanh Chương'), ('3290', 'Huyện Thanh Ba'), ('3289', 'Huyện Thạch An'), ('3288', 'Huyện Tương Dương'), ('3287', 'Huyện Tứ Kỳ'), ('3286', 'Huyện Tuyên Hóa'), ('3284', 'Huyện Tuy An'), ('3281', 'Huyện Tiền Hải'), ('3279', 'Huyện Tây Sơn'), ('3278', 'Huyện Tây Hòa'), ('3276', 'Huyện Tân Thạnh'), ('3275', 'Huyện Tân Phước'), ('3273', 'Huyện Tân Hưng'), ('3272', 'Huyện Tam Nông'), ('3271', 'Huyện Tam Đảo'), ('3270', 'Huyện Sơn Tây'), ('3267', 'Huyện Sơn Dương'), ('3266', 'huyện Sốp Cộp'), ('3265', 'Huyện Sông Lô'), ('3261', 'Huyện Quỳ Châu'), ('3260', 'Huyện Quế Phong'), ('3259', 'Huyện Quảng Uyên'), ('3258', 'Huyện Quảng Trạch'), ('3257', 'Huyện Quảng Điền'), ('3255', 'Huyện Phú Xuyên'), ('3254', 'Huyện Phù Mỹ'), ('3250', 'Huyện Phong Điền'), ('3249', 'Huyện Pác Nặm'), ('3247', 'Huyện Nho Quan'), ('3246', 'Huyện Nguyên Bình'), ('3243', 'Huyện Nghĩa Hưng'), ('3242', 'Huyện Ngân Sơn'), ('3241', 'Huyện Nga Sơn'), ('3238', 'Huyện Ninh Giang'), ('3234', 'Huyện Nam Đông'), ('3233', 'Huyện Nam Đàn'), ('3232', 'Huyện Na Rì'), ('3230', 'Huyện Mường La'), ('3227', 'Huyện Mộc Hóa'), ('3226', 'Huyện Mộ Đức'), ('3224', 'Huyện Minh Hóa'), ('3220', 'Huyện Lộc Hà'), ('3218', 'Thị xã Long Mỹ'), ('3217', 'Huyện Lắk'), ('3216', 'Huyện Lang Chánh'), ('3213', 'Huyện Khánh Vĩnh'), ('3212', 'Huyện Khánh Sơn'), ('3211', 'Huyện Kỳ Sơn'), ('3205', 'Huyện Kim Sơn'), ('3203', 'Huyện Kiến Thụy'), ('3201', 'Huyện Hương Sơn'), ('3200', 'Thành phố Hồng Ngự'), ('3199', 'Huyện Hoành Bồ'), ('3196', 'Huyện Hàm Tân'), ('3194', 'Huyện Hạ Lang'), ('3193', 'Huyện Giao Thủy'), ('3191', 'Huyện Gia Viễn'), ('3188', 'Huyện Đức Thọ'), ('3186', 'Huyện Đồng Xuân'), ('3185', 'Thị xã Đông Triều'), ('3184', 'Thị xã Đông Hòa'), ('3182', 'Huyện Đình Lập'), ('3180', 'Huyện Đầm Hà'), ('3160', 'Huyện Di Linh'), ('3158', 'Huyện Chợ Lách'), ('3157', 'Huyện Chiêm Hóa'), ('3156', 'Huyện Chi Lăng'), ('3155', 'Huyện Châu Thành'), ('3153', 'Huyện Cư Kuin'), ('3152', 'Huyện Cư Jút'), ('3150', 'Huyện Cờ Đỏ'), ('3147', 'Huyện Cẩm Thủy'), ('3146', 'Huyện Cát Tiên'), ('3143', 'Huyện Can Lộc'), ('3141', 'Huyện Bù Gia Mập'), ('3140', 'Huyện Bù Đốp'), ('3138', 'Huyện Bình Gia'), ('3135', 'Huyện Bắc Tân Uyên'), ('3134', 'Huyện Bắc Sơn'), ('3132', 'Huyện Bàu Bàng'), ('3130', 'Huyện Bảo Lạc'), ('3129', 'Huyện Bác Ái'), ('3127', 'Huyện Ba Tơ'), ('3126', 'Huyện Ba Chẽ'), ('3125', 'Huyện An Minh'), ('2272', 'Thị xã Vĩnh Châu'), ('2270', 'Huyện Yên Thủy'), ('2268', 'Huyện Yên Lập'), ('2267', 'Huyện Yên Châu'), ('2266', 'Huyện Yên Bình'), ('2264', 'Huyện Xi Ma Cai'), ('2263', 'Huyện Vũng Liêm'), ('2260', 'Huyện Vĩnh Thuận'), ('2258', 'Huyện Vĩnh Thạnh'), ('2256', 'Huyện Vị Xuyên'), ('2255', 'Huyện Vân Hồ'), ('2251', 'Huyện U Minh Thượng'), ('2249', 'Huyện Triệu Sơn'), ('2248', 'Huyện Trạm Tấu'), ('2239', 'Huyện Thăng Bình'), ('2238', 'Huyện Thạnh Trị'), ('2237', 'Huyện Thanh Thủy'), ('2227', 'Huyện Tuy Đức'), ('2225', 'Huyện Tu Mơ Rông'), ('2224', 'Huyện Tiên Phước'), ('2222', 'Huyện Tây Trà'), ('2219', 'Huyện Tây Giang'), ('2216', 'Huyện Tân Phú Đông'), ('2211', 'Huyện Sơn Hòa'), ('2210', 'Huyện Sơn Hà'), ('2206', 'Huyện Sông Hinh'), ('2205', 'Huyện Sa Thầy'), ('2204', 'Huyện Quỳnh Nhai'), ('2198', 'Huyện Phước Sơn'), ('2195', 'Huyện Phú Lương'), ('2194', 'Huyện Phù Cừ'), ('2193', 'Huyện Phong Điền'), ('2190', 'Huyện Như Thanh'), ('2187', 'Huyện Ngọc Hồi'), ('2186', 'Huyện Ngọc Hiển'), ('2182', 'Huyện Nông Sơn'), ('2181', 'Huyện Nông Cống'), ('2179', 'Huyện Nậm Pồ'), ('2178', 'Huyện Nam Trà My'), ('2177', 'Huyện Nam Giang'), ('2173', 'Huyện Mỹ Tú'), ('2171', 'Huyện Mường Khương'), ('2170', 'Huyện Mường Ảng'), ('2167', 'Huyện Minh Long'), ('2165', 'Huyện Mang Yang'), ('2164', 'Huyện Mang Thít'), ('2163', 'Huyện Mai Châu'), ('2161', 'Huyện Long Phú'), ('2157', 'Huyện Lạc Thủy'), ('2156', 'Huyện Lạc Sơn'), ('2152', 'Huyện Krông Pa'), ('2151', 'Huyện Krông Nô'), ('2150', 'Huyện Krông Búk'), ('2149', 'Huyện Kông Chro'), ('2148', 'Huyện Kon Rẫy'), ('2146', 'Huyện Kim Bôi'), ('2144', 'Huyện Kbang'), ('2140', 'Huyện Hoài Ân'), ('2139', 'Huyện Hiệp Đức'), ('2137', 'Huyện Hải Lăng'), ('2134', 'Huyện Giang Thành'), ('2132', 'Huyện Gò Quao'), ('2131', 'Huyện Ea Súp'), ('2129', 'Huyện Đức Huệ'), ('2125', 'Huyện Đông Giang'), ('2123', 'Huyện Điện Biên Đông'), ('2121', 'Huyện Đắk Tô'), ('2120', 'Huyện Đắk Song'), ('2119', 'Huyện Đắk Pơ'), ('2118', 'Huyện Đắk Đoa'), ('2117', 'Huyện đảo Trường Sa'), ('2116', 'Huyện đảo Phú Quý'), ('2115', 'Thành phố Phú Quốc'), ('2114', 'Huyện đảo Lý Sơn'), ('2113', 'Huyện đảo Kiên Hải'), ('2112', 'Huyện đảo Hoàng Sa'), ('2111', 'Huyện đảo Côn Đảo'), ('2110', 'Huyện đảo Cồn Cỏ'), ('2109', 'Huyện đảo Cô Tô'), ('2108', 'Huyện đảo Cát Hải'), ('2107', 'Huyện đảo Bạch Long Vĩ'), ('2106', 'Huyện Đạ Tẻh'), ('2105', 'Huyện Đa Krông'), ('2104', 'Huyện Đạ Huoai'), ('2103', 'Huyện Duyên Hải'), ('2101', 'Huyện Chư Pưh'), ('2096', 'Huyện Châu Thành'), ('2093', 'Huyện Cù Lao Dung'), ('2091', 'Huyện Cầu Kè'), ('2090', 'Huyện Cần Giờ'), ('2087', 'Huyện Cao Phong'), ('2086', 'Huyện Càng Long'), ('2084', 'Huyện Cai Lậy'), ('2081', 'Huyện Bình Tân'), ('2079', 'Huyện Bắc Yên'), ('2078', 'Huyện Bắc Trà My'), ('2075', 'Huyện Bắc Mê'), ('2073', 'Huyện Bảo Thắng'), ('2070', 'Huyện Bá Thước'), ('2066', 'Thị xã Quảng Yên'), ('2065', 'Thành phố Phúc Yên'), ('2064', 'Thị xã Phú Thọ'), ('2063', 'Thị xã Nghĩa Lộ'), ('2062', 'Thị xã Ngã Năm'), ('2061', 'Thị xã Ninh Hòa'), ('2060', 'Thị xã Mường Lay'), ('2059', 'Thị xã Hồng Ngự'), ('2058', 'Thành phố Hà Tiên'), ('2057', 'Thị xã Gò Công'), ('2056', 'Thành phố Chí Linh'), ('2055', 'Thị xã Cai Lậy'), ('2054', 'Thị xã Bình Minh'), ('2053', 'Huyện Yên Minh'), ('2052', 'Huyện Xín Mần'), ('2051', 'Huyện Võ Nhai'), ('2050', 'Huyện Vĩnh Lợi'), ('2049', 'Huyện Vĩnh Cửu'), ('2048', 'Huyện Vị Thuỷ'), ('2047', 'Huyện Văn Yên'), ('2046', 'Huyện Văn Lâm'), ('2045', 'Huyện Văn Giang'), ('2044', 'Huyện Văn Chấn'), ('2043', 'Huyện Văn Bàn'), ('2042', 'Huyện U Minh'), ('2041', 'Huyện Trùng Khánh'), ('2040', 'Huyện Triệu Phong'), ('2039', 'Huyện Trấn Yên'), ('2038', 'Huyện Trần Văn Thời'), ('2037', 'Huyện Trần Đề'), ('2036', 'Huyện Tràng Định'), ('2035', 'Thị xã Trảng Bàng'), ('2034', 'Huyện Trà Ôn'), ('2033', 'Huyện Trà Cú'), ('2032', 'Huyện Thuận Châu'), ('2031', 'Huyện Thủ Thừa'), ('2030', 'Huyện Tháp Mười'), ('2029', 'Huyện Thanh Sơn'), ('2028', 'Huyện Thạnh Phú'), ('2027', 'Huyện Thanh Liêm'), ('2026', 'Huyện Thanh Bình'), ('2025', 'Huyện Than Uyên'), ('2024', 'Huyện Thạch Hà'), ('2023', 'Huyện Tuy Phước'), ('2022', 'Huyện Tuần Giáo'), ('2021', 'Huyện Tủa Chùa'), ('2020', 'Huyện Tiểu Cần'), ('2019', 'Huyện Tiên Yên'), ('2018', 'Huyện Tiên Lữ'), ('2017', 'Huyện Tân Uyên'), ('2016', 'Huyện Tân Trụ'), ('2015', 'Huyện Tân Sơn'), ('2014', 'Huyện Tân Lạc'), ('2013', 'Huyện Tân Hồng'), ('2012', 'Huyện Tánh Linh'), ('2011', 'Huyện Tam Nông'), ('2010', 'Huyện Tam Đường'), ('2009', 'Huyện Tam Dương'), ('2008', 'Huyện Tam Bình'), ('2007', 'Huyện Sông Mã'), ('2006', 'Huyện Sìn Hồ'), ('2005', 'Thị xã Sa Pa'), ('2004', 'Huyện Quốc Oai'), ('2003', 'Huyện Quế Sơn'), ('2002', 'Huyện Quảng Ninh'), ('2001', 'Huyện Quang Bình'), ('2000', 'Huyện Quan Sơn'), ('1999', 'Huyện Quản Bạ'), ('1998', 'Huyện Phước Long'), ('1997', 'Huyện Phục Hòa'), ('1996', 'Huyện Phù Yên'), ('1995', 'Huyện Phú Ninh'), ('1994', 'Huyện Phù Ninh'), ('1993', 'Huyện Phú Hòa'), ('1992', 'Huyện Phú Giáo'), ('1991', 'Huyện Phú Bình'), ('1990', 'Thị xã Phổ Yên'), ('1989', 'Huyện Phong Thổ'), ('1988', 'Huyện Nghĩa Hành'), ('1987', 'Huyện Núi Thành'), ('1986', 'Huyện Ninh Phước'), ('1985', 'Huyện Ninh Hải'), ('1984', 'Huyện Nậm Nhùn'), ('1983', 'Huyện Nam Trực'), ('1982', 'Huyện Na Hang'), ('1981', 'Huyện Mỹ Lộc'), ('1980', 'Huyện Mường Tè'), ('1979', 'Huyện Mường Nhé'), ('1978', 'Huyện Mường Chà'), ('1977', 'Huyện Mù Cang Chải'), ('1976', 'Huyện Mộc Châu'), ('1975', 'Huyện Mỏ Cày Nam'), ('1974', 'Huyện Mỏ Cày Bắc'), ('1973', 'Huyện Mèo Vạc'), ('1971', 'Huyện Mai Sơn'), ('1970', 'Huyện Lý Nhân'), ('1969', 'Huyện Lương Tài'), ('1968', 'Huyện Lương Sơn'), ('1967', 'Huyện Lục Yên'), ('1966', 'Huyện Lục Ngạn'), ('1965', 'Huyện Lục Nam'), ('1964', 'Huyện Lộc Ninh'), ('1963', 'Huyện Lộc Bình'), ('1962', 'Huyện Long Hồ'), ('1961', 'Huyện Lấp Vò'), ('1960', 'Huyện Lập Thạch'), ('1959', 'Huyện Lâm Thao'), ('1958', 'Huyện Lâm Hà'), ('1957', 'Huyện Lâm Bình'), ('1956', 'Huyện Lạc Dương'), ('1955', 'Huyện Kỳ Sơn'), ('1954', 'Huyện Krông Pắc'), ('1953', 'Huyện Kim Thành'), ('1952', 'Huyện Kim Bảng'), ('1951', 'Huyện Kiến Xương'), ('1950', 'Huyện Kiên Lương'), ('1949', 'Huyện Kế Sách'), ('1948', 'Huyện Hữu Lũng'), ('1947', 'Huyện Hưng Nguyên'), ('1946', 'Huyện Hồng Dân'), ('1945', 'Huyện Hoàng Su Phì'), ('1944', 'Huyện Hoa Lư'), ('1943', 'Huyện Hòa An'), ('1942', 'Huyện Hậu Lộc'), ('1941', 'Huyện Hàm Yên'), ('1940', 'Huyện Hải Hà'), ('1939', 'Huyện Hà Quảng'), ('1938', 'Huyện Hạ Hòa'), ('1937', 'Huyện Giồng Trôm'), ('1936', 'Huyện Gio Linh'), ('1935', 'Thị Xã Giá Rai'), ('1934', 'Huyện Gia Lộc'), ('1933', 'Huyện Gò Công Tây'), ('1932', 'Huyện Gò Công Đông'), ('1931', 'Huyện Ea Kar'), ('1930', 'Thị xã Đức Phổ'), ('1929', 'Huyện Đức Hòa'), ('1928', 'Huyện Đồng Văn'), ('1927', 'Huyện Đông Sơn'), ('1926', 'Huyện Đông Hải'), ('1925', 'Huyện Đoan Hùng'), ('1924', 'Huyện Định Hóa'), ('1923', 'Huyện Điện Biên'), ('1922', 'Huyện Đầm Dơi'), ('1921', 'Huyện Đắk Glei'), ('1920', 'Huyện đảo Vân Đồn'), ('1919', 'Huyện Đam Rông'), ('1918', 'Huyện Đại Từ'), ('1917', 'Huyện Đại Lộc'), ('1916', 'Huyện Đà Bắc'), ('1915', 'Huyện Chương Mỹ'), ('1914', 'Huyện Chợ Mới'), ('1913', 'Huyện Chợ Đồn'), ('1912', 'Huyện Châu Thành A'), ('1911', 'Huyện Châu Thành'), ('1910', 'Huyện Châu Thành'), ('1909', 'Huyện Châu Thành'), ('1908', 'Huyện Cầu Ngang'), ('1907', 'Huyện Cần Giuộc'), ('1906', 'Huyện Cần Đước'), ('1905', 'Huyện Cẩm Khê'), ('1904', 'Huyện Cao Lộc'), ('1903', 'Huyện Cam Lộ'), ('1902', 'Huyện Cam Lâm'), ('1901', 'Huyện Cái Nước'), ('1900', 'Huyện Cái Bè'), ('1899', 'Huyện Bù Đăng'), ('1898', 'Huyện Bình Sơn'), ('1897', 'Huyện Bình Lục'), ('1896', 'Huyện Bình Liêu'), ('1895', 'Huyện Bình Đại'), ('1894', 'Huyện Bến Lức'), ('1893', 'Huyện Bắc Quang'), ('1892', 'Huyện Bắc Hà'), ('1891', 'Huyện Bảo Yên'), ('1890', 'Huyện Bảo Lâm'), ('1889', 'Huyện Bạch Thông'), ('1888', 'Huyện Ba Tri'), ('1887', 'Huyện Ba Bể'), ('1886', 'Huyện An Lão'), ('1885', 'Huyện A Lưới'), ('1884', 'Huyện Krông Ana'), ('1883', 'Huyện Phú Tân'), ('1882', 'Huyện Phú Lộc'), ('1881', 'Huyện Vĩnh Lộc'), ('1880', 'Huyện Thạch Thành'), ('1879', 'Huyện Quan Hóa'), ('1878', 'Huyện Mường Lát'), ('1877', 'Huyện Hà Trung'), ('1876', 'Thị xã Bỉm Sơn'), ('1875', 'Huyện Yên Định'), ('1874', 'Huyện Ngọc Lặc'), ('1873', 'Huyện Thọ Xuân'), ('1872', 'Huyện Thường Xuân'), ('1871', 'Huyện Như Xuân'), ('1870', 'Thị Xã Nghi Sơn'), ('1869', 'Huyện Thái Thụy'), ('1868', 'Huyện Quỳnh Phụ'), ('1867', 'Huyện Hưng Hà'), ('1866', 'Huyện Gò Dầu'), ('1865', 'Huyện Bến Cầu'), ('1864', 'Huyện Dương Minh Châu'), ('1863', 'Huyện Tân Châu'), ('1862', 'Huyện Tân Biên'), ('1861', 'Huyện Vĩnh Linh'), ('1860', 'Huyện Hướng Hóa'), ('1859', 'Thị xã Ba Đồn'), ('1858', 'Huyện Bố Trạch'), ('1857', 'Huyện Lệ Thủy'), ('1856', 'Thị Xã Sông Cầu'), ('1855', 'Huyện Ninh Sơn'), ('1854', 'Huyện Nghi Lộc'), ('1853', 'Huyện Con Cuông'), ('1852', 'Huyện Quỳ Hợp'), ('1851', 'Huyện Nghĩa Đàn'), ('1850', 'Thị xã Thái Hòa'), ('1849', 'Thị xã Hoàng Mai'), ('1848', 'Huyện Quỳnh Lưu'), ('1847', 'Huyện Diễn Châu'), ('1846', 'Huyện Yên Thành'), ('1845', 'Huyện Tân Kỳ'), ('1844', 'Huyện Anh Sơn'), ('1843', 'Huyện Đô Lương'), ('1842', 'Thị xã Cửa Lò'), ('1841', 'Huyện Ý Yên'), ('1840', 'Huyện Hải Hậu'), ('1839', 'Huyện Bảo Lâm'), ('1838', 'Thành phố Bảo Lộc'), ('1837', 'Huyện Đức Trọng'), ('1836', 'Huyện Đơn Dương'), ('1835', 'Huyện Đắk Hà'), ('1834', 'Huyện Kon Plông'), ('1833', 'Huyện An Biên'), ('1832', 'Huyện Giồng Riềng'), ('1831', 'Huyện Tân Hiệp'), ('1830', 'Huyện Hòn Đất'), ('1829', 'Huyện Vạn Ninh'), ('1828', 'Huyện Yên Mỹ'), ('1827', 'Thị xã Mỹ Hào'), ('1826', 'Huyện Khoái Châu'), ('1825', 'Huyện Ân Thi'), ('1824', 'Huyện Phụng Hiệp'), ('1823', 'Thành phố Ngã Bảy'), ('1822', 'Huyện Vĩnh Bảo'), ('1821', 'Huyện Tiên Lãng'), ('1820', 'Huyện An Lão'), ('1819', 'Huyện An Dương'), ('1818', 'Thị xã Kinh Môn'), ('1817', 'Huyện Cẩm Giàng'), ('1816', 'Huyện Bình Giang'), ('1815', 'Huyện Cẩm Xuyên'), ('1814', 'Thị xã Hồng Lĩnh'), ('1813', 'Huyện Nghi Xuân'), ('1812', 'Huyện Hương Khê'), ('1811', 'Huyện Kỳ Anh'), ('1810', 'Huyện Ứng Hòa'), ('1809', 'Huyện Thanh Oai'), ('1808', 'Huyện Thạch Thất'), ('1807', 'Huyện Phúc Thọ'), ('1806', 'Huyện Mỹ Đức'), ('1805', 'Huyện Hoài Đức'), ('1804', 'Huyện Đan Phượng'), ('1803', 'Huyện Ba Vì'), ('1802', 'Thị xã Duy Tiên'), ('1801', 'Huyện Chư Păh'), ('1800', 'Thị xã An Khê'), ('1799', 'Huyện Ia Pa'), ('1798', 'Thị xã Ayun Pa'), ('1797', 'Huyện Phú Thiện'), ('1796', 'Huyện Chư Sê'), ('1795', 'Huyện Chư Prông'), ('1794', 'Huyện Đức Cơ'), ('1793', 'Huyện Ia Grai'), ('1792', 'Huyện Đắk Mil'), ('1791', 'Huyện Đắk Glong'), ('1790', 'Huyện Đắk R lấp'), ('1789', 'Huyện Krông Bông'), ('1788', 'Thị xã Buôn Hồ'), ('1787', 'Huyện Krông Năng'), ('1786', 'Huyện Ea H leo'), ('1785', 'Huyện Cư M gar'), ('1784', 'Huyện Buôn Ðôn'), ('1783', 'Huyện Năm Căn'), ('1782', 'Huyện Thới Bình'), ('1781', 'Huyện Tuy Phong'), ('1780', 'Huyện Bắc Bình'), ('1779', 'Huyện Đức Linh'), ('1778', 'Thị xã La Gi'), ('1777', 'Huyện Hàm Thuận Bắc'), ('1776', 'Huyện Hàm Thuận Nam'), ('1775', 'Thị xã Phước Long'), ('1774', 'Thị xã Bình Long'), ('1773', 'Huyện Hớn Quản'), ('1772', 'Huyện Chơn Thành'), ('1771', 'Thị xã Hoài Nhơn'), ('1770', 'Huyện Phù Cát'), ('1769', 'Thị xã An Nhơn'), ('1768', 'Huyện Yên Phong'), ('1767', 'Huyện Thuận Thành'), ('1766', 'Huyện Gia Bình'), ('1765', 'Huyện Yên Thế'), ('1764', 'Huyện Yên Dũng'), ('1763', 'Huyện Việt Yên'), ('1762', 'Huyện Tân Yên'), ('1761', 'Huyện Sơn Động'), ('1760', 'Huyện Lạng Giang'), ('1759', 'Huyện Hiệp Hòa'), ('1758', 'Huyện Châu Phú'), ('1757', 'Huyện Chợ Mới'), ('1756', 'Huyện Phú Tân'), ('1755', 'Huyện Tân Châu'), ('1754', 'Huyện An Phú'), ('1753', 'Thành phố Châu Đốc'), ('1752', 'Huyện Tịnh Biên'), ('1751', 'Huyện Tri Tôn'), ('1750', 'Huyện Thoại Sơn'), ('1749', 'Huyện Phú Vang'), ('1748', 'Huyện Hoằng Hóa'), ('1747', 'Huyện Quảng Xương'), ('1746', 'Huyện Dầu Tiếng'), ('1745', 'Huyện Yên Sơn'), ('1744', 'Huyện Bát Xát'), ('1743', 'Huyện Mỹ Xuyên'), ('1742', 'Huyện Châu Thành'), ('1741', 'Huyện Chợ Gạo'), ('1740', 'Huyện Châu Thành'), ('1739', 'Huyện Diên Khánh'), ('1738', 'Huyện Tư Nghĩa'), ('1737', 'Huyện Sơn Tịnh'), ('1736', 'Thị xã Điện Bàn'), ('1735', 'Huyện Duy Xuyên'), ('1734', 'Huyện Yên Lạc'), ('1733', 'Huyện Vĩnh Tường'), ('1732', 'Huyện Bình Xuyên'), ('1731', 'Huyện Đồng Hỷ'), ('1730', 'Thị xã Từ Sơn'), ('1729', 'Huyện Tiên Du'), ('1728', 'Huyện Quế Võ'), ('1727', 'Huyện Nam Sách'), ('1726', 'Huyện Thủy Nguyên'), ('1725', 'Huyện Lai Vung'), ('1724', 'Huyện Cao Lãnh'), ('1723', 'Huyện Hòa Bình'), ('1722', 'Huyện Đồng Phú'), ('1721', 'Thị xã Hòa Thành'), ('1720', 'Huyện Châu Thành'), ('1719', 'Huyện Châu Thành'), ('1718', 'Huyện Châu Thành'), ('1717', 'Huyện Kim Động'), ('1716', 'Huyện Vũ Thư'), ('1715', 'Huyện Đông Hưng'), ('1714', 'Huyện Yên Khánh'), ('1713', 'Thành phố Tam Điệp'), ('1712', 'Thành phố Sầm Sơn'), ('1711', 'Thị xã Sơn Tây'), ('1710', 'Huyện Thanh Trì'), ('1709', 'Huyện Châu Đức'), ('1708', 'Huyện Nhơn Trạch'), ('1707', 'Quận Đồ Sơn'), ('1706', 'Quận Dương Kinh'), ('1705', 'Huyện Thống Nhất'), ('1704', 'Huyện Xuân Lộc'), ('1703', 'Huyện Gia Lâm'), ('1702', 'Huyện Cẩm Mỹ'), ('1701', 'Thị Xã Phú Mỹ'), ('1700', 'Huyện Định Quán'), ('1699', 'Huyện Xuyên Mộc'), ('1698', 'Thị xã Hương Thủy'), ('1697', 'Thị xã Hương Trà'), ('1696', 'Thị xã Bến Cát'), ('1695', 'Thị xã Tân Uyên'), ('1694', 'Huyện Long Thành'), ('1693', 'Huyện Tân Phú'), ('1692', 'Thành phố Long Khánh'), ('1691', 'Huyện Trảng Bom'), ('1690', 'Huyện Đất Đỏ'), ('1689', 'Huyện Long Điền'), ('1688', 'TT Phú Mỹ - cũ'), ('1687', 'Huyện Hòa Vang'), ('1686', 'Thành phố Uông Bí'), ('1684', 'Thành Phố Sông Công'), ('1683', 'Thành phố Cẩm Phả'), ('1682', 'Thành phố Lào Cai'), ('1680', 'Thành phố Hưng Yên'), ('1678', 'Thành phố Hòa Bình'), ('1677', 'Thành phố Sơn La'), ('1676', 'Thành phố Điện Biên Phủ'), ('1675', 'Thành phố Lai Châu'), ('1674', 'Thành phố Yên Bái'), ('1668', 'Thành phố Sa Đéc'), ('1667', 'Thành phố Bà Rịa'), ('1666', 'Thành phố Phan Thiết'), ('1665', 'Thành phố Phan Rang – Tháp Chàm'), ('1664', 'Thành phố Cam Ranh'), ('1663', 'Thành phố Tuy Hòa'), ('1662', 'Thành phố Quy Nhơn'), ('1660', 'Thành phố Kon Tum'), ('1655', 'Thành phố Bạc Liêu'), ('1654', 'Thành phố Cà Mau'), ('1653', 'Thành phố Vị Thanh'), ('1652', 'Long An'), ('1644', 'Thành phố Bắc Ninh'), ('1643', 'Thành phố Bắc Giang'), ('1642', 'Thành phố Lạng Sơn'), ('1641', 'Thành phố Cao Bằng'), ('1640', 'Thành phố Bắc Kạn'), ('1639', 'Thành phố Thái Nguyên'), ('1632', 'Thành phố Hội An'), ('1631', 'Thành phố Tam Kỳ'), ('1630', 'Thành phố Quảng Ngãi'), ('1627', 'Thành phố Gia Nghĩa'), ('1626', 'Thành phố Tây Ninh'), ('1625', 'Thành phố Đồng Xoài'), ('1621', 'Thị xã Quảng Trị'), ('1620', 'Thành phố Đông Hà'), ('1619', 'Thành phố Đồng Hới'), ('1618', 'Thành phố Hà Tĩnh'), ('1617', 'Thành phố Vinh'), ('1616', 'Thành phố Thanh Hóa'), ('1615', 'Thành phố Ninh Bình'), ('1614', 'Thành phố Phủ Lý'), ('1613', 'Thành phố Nam Định'), ('1604', 'Thành phố Hạ Long'), ('1603', 'Thành phố Móng Cái'), ('1602', 'Thành phố Việt Trì'), ('1601', 'Thành phố Tuyên Quang'), ('1600', 'Thành phố Hà Giang'), ('1599', 'Thành phố Thái Bình'), ('1598', 'Thành phố Hải Dương'), ('1591', 'Quận Hải An'), ('1590', 'Quận Kiến An'), ('1589', 'Quận Hồng Bàng'), ('1588', 'Quận Lê Chân'), ('1587', 'Quận Ngô Quyền'), ('1585', 'Thành phố Huế'), ('1583', 'Huyện Sóc Sơn'), ('1582', 'Huyện Đông Anh'), ('1581', 'Huyện Mê Linh'), ('1580', 'Quận Đặc Biệt'), ('1578', 'Thành phố Vĩnh Yên'), ('1576', 'Quận Thốt Nốt'), ('1575', 'Quận Ô Môn'), ('1574', 'Quận Cái Răng'), ('1573', 'Quận Bình Thủy'), ('1572', 'Quận Ninh Kiều'), ('1570', 'Thành phố Rạch Giá'), ('1568', 'Thành phố Sóc Trăng'), ('1566', 'Thành phố Long Xuyên'), ('1564', 'Thành phố Cao Lãnh'), ('1562', 'Thành phố Vĩnh Long'), ('1560', 'Thành phố Trà Vinh'), ('1558', 'Thành phố Bến Tre'), ('1556', 'Thành phố Mỹ Tho'), ('1554', 'Thành phố Tân An'), ('1552', 'Thành phố Buôn Ma Thuột'), ('1550', 'Thành phố Đà Lạt'), ('1548', 'Thành phố Nha Trang'), ('1546', 'Thành phố Pleiku'), ('1544', 'Thành phố Vũng Tàu'), ('1542', 'Quận Hà Đông'), ('1541', 'Thành phố Thuận An'), ('1540', 'Thành phố Dĩ An'), ('1538', 'Thành phố Thủ Dầu Một'), ('1536', 'Thành phố Biên Hòa'), ('1534', 'Huyện Nhà Bè'), ('1533', 'Huyện Bình Chánh'), ('1531', 'Quận Cẩm Lệ'), ('1530', 'Quận Liên Chiểu'), ('1529', 'Quận Ngũ Hành Sơn'), ('1528', 'Quận Sơn Trà'), ('1527', 'Quận Thanh Khê'), ('1526', 'Quận Hải Châu'), ('1493', 'Quận Thanh Xuân'), ('1492', 'Quận Tây Hồ'), ('1491', 'Quận Long Biên'), ('1490', 'Quận Hoàng Mai'), ('1489', 'Quận Hoàn Kiếm'), ('1488', 'Quận Hai Bà Trưng'), ('1486', 'Quận Đống Đa'), ('1485', 'Quận Cầu Giấy'), ('1484', 'Quận Ba Đình'), ('1482', 'Quận Bắc Từ Liêm'), ('1463', 'Quận Thủ Đức'), ('1462', 'Quận Bình Thạnh'), ('1461', 'Quận Gò Vấp'), ('1460', 'Huyện Củ Chi'), ('1459', 'Huyện Hóc Môn'), ('1458', 'Quận Bình Tân'), ('1457', 'Quận Phú Nhuận'), ('1456', 'Quận Tân Phú'), ('1455', 'Quận Tân Bình'), ('1454', 'Quận 12'), ('1453', 'Quận 11'), ('1452', 'Quận 10'), ('1451', 'Quận 9'), ('1450', 'Quận 8'), ('1449', 'Quận 7'), ('1448', 'Quận 6'), ('1447', 'Quận 5'), ('1446', 'Quận 4'), ('1444', 'Quận 3'), ('1443', 'Quận 2'), ('1442', 'Quận 1')], max_length=50),
        ),
    ]