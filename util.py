import jdatetime
def date_convertor(jdate):
    year, month, day = map(int, jdate.split("/"))
    jalali_date = jdatetime.date(year, month, day)
    return jalali_date.togregorian()
    