import pandas as pd
from compare import comparator, COMPARISONS


product1 = [{'asin': 'B0DLK83KCD', 
             'availability': {'message': 'Only 17 left in stock - order soon.', 'type': 'IN_STOCK_SCARCE'}, 
             'country': 'US', 
             'currency': 'USD', 
             'description': '', 
             'price': '46.99', 
             'product_details': ['ASIN: B0DLK83KCD', 'Date First Available: January 5, 2025', 'Manufacturer: A-NAFTULY', 'Brand: A-NAFTULY', 'Model: 751-739', 'Item Weight: 3.5 pounds', 'Package Dimensions: 21 x 11.5 x 3.25 inches', 'Item model number: Front Driver Side 751-739', 'Exterior: Polished', 'Manufacturer Part Number: AN70291&292', 'Position: Front Left', 'Package Dimensions: 21 x 11.5 x 3.25 inches; 3.5 Pounds'], 
             'product_images': ['https://m.media-amazon.com/images/I/31QSan1EsAL._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/51quz7VaZFL._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/51hbb2Hk15L._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/51iN-z04oIL._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/51UoF+e9A2L._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/519XacjxHAL._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/51KnPTxe07L._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/410K1PVfmCL._AC_SL500_.jpg', 
                                'https://m.media-amazon.com/images/I/51SB37Gev8L._AC_SL500_.jpg'], 
            'product_info': ['[Vehicle Fitment]: This front left window regulator with 2 pin motor fit for Chevy Cruze Limited 2016, Chevrolet Cruze 4/26/2012 2013 2014 2015, without anti-pinch & express up and down function, not for the window regulator with 7 pins window lift motor', '[OEM Part Number]: 751-739, 751739, 95382556, 95919259, 95265280, 95226749, 95382561, 95265273', '[Location]: Front left driver side, come with motor', '[Effortless Installation]: Original car hole position, power window lift regulator plug and play, no wire splicing is necessary, saving you time and effort', '[Package Content]: 1x Window regulator and motor assembly. we offer 2 year worry-free-warranty, If you encounter any issues with the door window regulator, our dedicated customer service team is here to assist you'], 
            'product_reviews': {'count': None, 'rating': None}, 
            'product_variations': {'color': [], 'size': []}, 
            'product_videos': [], 'quantity': {'max': 17, 'min': 1}, 
            'title': '751-739 Front Driver Side Power Window Regulator w/Motor (2 Pins) Fit for Chevy Cruze 2012 2013 2014 2015,Chevrolet Cruze Limited 2016,w/o Express Up and Down', 
            'url': ['https://www.amazon.com/751-739-Front-Driver-Side-Regulator/dp/B0DLK83KCD']}]

product2 = [{'asin': 'B0CJLRPZX1', 
             'availability': {'message': 'In Stock', 'type': 'IN_STOCK'}, 
             'country': 'US', 
             'currency': 'USD', 
             'description': 'A window regulator with excellent quality can provide Smooth and Quiet Operation environment for the passenger, Enhancing the overall driving experience for passengers', 
             'price': '35.99', 
             'product_details': ['Brand: Torchbeam', 'Model Name: Power Window Regulator', 'Material: Alloy Steel', 'Manufacturer: Torchbeam', 'Global Trade Identification Number: 06977814476649', 'ASIN: B0CJLRPZX1', 'Date First Available: September 22, 2023', 'Model: Power Window Regulator', 'Item Weight: 4.24 pounds', 'Product Dimensions: 23.62 x 13.78 x 2.76 inches', 'Item model number: 749-974', 'Exterior: Painted', 'Manufacturer Part Number: 7326PWR1312US', 'Product Dimensions: 23.62 x 13.78 x 2.76 inches; 4.25 Pounds', 'Material Type: Alloy Steel', 'Model: 749-974', 'Brand Name: Torchbeam'], 
             'product_images': ['https://m.media-amazon.com/images/I/41pV4rm9aEL._AC_SL500_.jpg', 'https://m.media-amazon.com/images/I/51WcG5c81YL._AC_SL500_.jpg', 'https://m.media-amazon.com/images/I/41i0cIU8PWL._AC_SL500_.jpg', 'https://m.media-amazon.com/images/I/418-Z6bhNiL._AC_SL500_.jpg', 'https://m.media-amazon.com/images/I/412HeAqF8tL._AC_SL500_.jpg', 'https://m.media-amazon.com/images/I/414ozDPEkGL._AC_SL500_.jpg', 'https://m.media-amazon.com/images/I/41uFT1rHb8L._AC_SL500_.jpg'], 
             'product_info': ['[Compatibility List] Front Driver Side Power Window Regulator fit for Cruze 2011-2015, Cruze Limited 2016-2016. Replace Part Number: 749-974, 384118; APWR0456; WLR2001; 95226749; 95265273; 95382561.', '[High-strength Materials] Torchbeam Window Regulator consists of a strong lifting bracket insures efficient operation and longer durability. Thickened steel cable and capped ends resist commonly break or causing pull through.', '[Premium Quality] Torchbeam replacement power window regulator undergoes precise engineering design and rigorous testing to match the fit, function and performance of the original window regulator on specified vehicles', '[Enhancing Driving Experience] A window regulator with excellent quality can provide Smooth and Quiet Operation environment for the passenger, Enhancing the overall driving experience for passengers', '[Warm Tips] Please confirm that this Power Window Regulator fits your vehicle (Year+Make+Model+Engine+Applicable Position) before buying!'], 
             'product_reviews': {'count': 5, 'rating': 4.7}, 
             'product_variations': {'color': [], 'size': []}, 
             'product_videos': [], 'quantity': {'max': 30, 'min': 1}, 
             'title': 'Torchbeam Front Driver Side Power Window Regulator Without Motor, 749-974 Replace for Cruze 2011-2015, Cruze Limited 2016', 
             'url': ['https://www.amazon.com/Torchbeam-Regulator-Without-749-974-2011-2015/dp/B0CJLRPZX1']}]



product1 = comparator(product1)
product2 = comparator(product2)

def constr_comp(products):
    dfp = []
    for p in products:
        title = p['title']
        currency = p['currency']
        price = p['price']
        description = p['description']
        details = p['details']
        images = p['images']
        reviews = p['reviews']
        url = p['url'][0]

        dfp.append([title, currency, price, description, details, images, reviews, url])


    df = pd.DataFrame({'Product 1' : dfp[0],
                       'Product 2' : dfp[1]}, index = COMPARISONS)

    print(df)

constr_comp([product1, product2])