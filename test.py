import easyocr
reader = easyocr.Reader(['pt','en']) # need to run only once to load model into memory
result = reader.readtext('./uploads/3.jpg', detail = 0)
res = " ".join(result)
print(res)