cdef extern from "great_circle.h":
    void great_circle (double lon1, double lat1, double lon2, double lat2)

def py_great_circle(lon1, lat1, lon2, lat2):
    great_circle(lon1, lat1, lon2, lat2)
