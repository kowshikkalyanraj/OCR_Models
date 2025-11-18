# database.py
# ------------------------------------------------------------
# Stores all unique OCR label text extractions
# Each entry is a multi-line string representing one label.
# ------------------------------------------------------------

ocr_labels = [

    # Label 1: Joshua Ramsay
    """
    US POSTAGE & FEES PAID
    PRIORITY MAIL 2- DAY™
    NOTIFII LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    C014
    SHIP TO:
    Joshua Ramsay
    Pico Lanai
    2501 Pico Blvd.
    Santa Monica CA 90405-1832
    USPS SIGNATURE TRACKING #
    9410 8116 9900 0799 4639 52
    """,

    # Label 2: Pamela Stevens
    """
    US POSTAGE & FEES PAID
    PRIORITY MAIL 2-DAY™
    NOTIFII LLC
    8150 SIERRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    SHIP TO:
    Pamela Stevens
    Villas at Bandera
    9830 Camino Villa Office
    San Antonio TX 78254-5696
    USPS SIGNATURE TRACKING #
    9410 8116 990C 0602 5131 40
    """,

    # Label 3: Elaine Penman
    """
    US POSTAGE & FEES PAID
    PRIORITY MAIL 2-DAY™
    NOTIFII LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    C015
    SHIP TO:
    Elaine Penman
    The District on 5th
    550 N. 5th Avenue
    Tucson AZ 85705-8420
    USPS TRACKING #
    9405 5116 9900 0769 6885 66
    """,

    # Label 4: Janelle DeGrafft
    """
    US POSTAGE & FEES PAID
    PRIORITY MAIL 2-DAY™
    NOTIFII LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    SHIP TO:
    Janelle DeGrafft
    TEN M Flats
    10101 Twin Rivers Road
    Columbia MD 21044-2675
    USPS SIGNATURE TRACKING #
    9410 8116 9900 0603 5745 84
    """,

    # Label 5: Lencare (Ray) Sanders
    """
    US POSTAGE & FEES PAID
    PRIORITY MAIL 2-DAY™
    NOTIFII LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    SHIP TO:
    Lencare (Ray) Sanders
    Detroit Lions
    2000 Brush Street Suite 200
    Detroit MI 48226-2251
    USPS SIGNATURE TRACKING #
    9410 8116 9900 0437 8062 33
    """,

    # Label 6: Ashley Scharr
    """
    PRIORITY MAIL 2-DAY™
    NOTIFII LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    SHIP TO:
    Ashley Scharr
    The National WWII Museum
    945 Magazine Street
    New Orleans LA 70130-3813
    USPS SIGNATURE TRACKING #
    9410 8116 9900 0910 9790 34
    """,

    # Label 7: Sheridan LaFrance
    """
    PRIORITY MAIL 2-DAY™
    NOTIFII LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    SHIP TO:
    Sheridan LaFrance
    The Mayfair Apartment Homes
    4254 Maple Leaf Dr
    New Orleans LA 70131-7425
    USPS SIGNATURE TRACKING #
    9410 8116 9900 0662 6454 47
    """,

    # Label 8: Syta Saephan
    """
    DSR2
    Syta Saephan
    2821 CARRADALE DR
    ROSEVILLE CA 95661-4047
    United States
    Not restricted as per special provision
    A123
    TBA323546288697
    """,

    # Label 9: Ky Dong
    """
    Ky Dong
    2821 CARRADALE DR
    ROSEVILLE CA 95661-4047
    09/13 Same Auto
    0.7 Lbs
    Btw2jc6H0/2/4021
    IMG_0996.JPEG
    TBA324327178882
    """,

    # Label 10: Zoey Dong
    """
    Zoey Dong
    2821 CARRADALE DR
    ROSEVILLE CA 95661-4047
    08/21
    CYCLE 1
    0.4 Lbs
    BWqvxFLX6/1/304
    IMG_09951.JPEG
    TBA323777552487
    """,

    # Label 11: Syta Saephan (2nd entry)
    """
    Syta Saephan
    2821 CARRADALE DR
    ROSEVILLE CA 95661-4047
    10/03
    CYCLE 1
    0.3 Lbs
    TBA324798792651
    IMG_1002.JPEG
    """,

    # Label 12: Binh Hoan
    """
    WHITE LLC
    8150 SRRA COLLEGE BLVD SUITE 230
    ROSEVILLE CA 95661
    SHIP TO:
    Binh Hoan
    Orange County Public Works
    601 N Ross Street
    Santa Ana CA 92701
    USPS SIGNATURE TRACKING #
    9410 8116 9900 0348 2251 23
    """
]
