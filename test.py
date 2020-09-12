import easyocr
reader = easyocr.Reader(['pt','en']) # need to run only once to load model into memory
result = reader.readtext('./uploads/ee970df0-30f8-4309-9ef7-5fdb048a5ed8.jpeg', detail = 0)
res = " ".join(result)
print(res)