import re
import zlib
import cv2

from scapy.all import *

pictures_directory = "Pictures"
faces_directory = "faces"
pcap_file = "arper.pcap"


def face_detect(path,file_name):

    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

    if len(rects)==0:
        return False

    rects[:,2:]+=rects[:,:2]
    for x1,y1,x2,y2 in rects:
        cv2.rectangle(img,(x1,y1),(x2,y2),(127,255,0),2)

    cv2.imwrite("%s/%s-%s" % (faces_directory,pcap_file,file_name),img)

    return True


def get_http_header(http_payload):
    try:
        header_raw=http_payload[:http_payload.index("\r\n\r\n")+2]

        headers=dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",header_raw))

    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers


def extract_image(headers,http_payload):

    image =None
    image_type=None

    try:
        # print headers
        if "image" in headers["Content-Type"] and headers["Content-Length"]!= "0":

            # print http_payload

            image_type=headers["Content-Type"].split('/')[1]

            image=http_payload[http_payload.index("\r\n\r\n")+9:]

            print image

            try:
                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image=zlib.decompress(image,16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image=zlib.decompress(image)

            except:
                pass

    except:
        return None,None

    return image,image_type



def http_assemble(pcap_file):

    carved_images = 0
    faces_detect = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()
    # print sessions
    for session in sessions:
        # print session
        http_payload = ""

        for packets in sessions[session]:
            # print packets
            try:
                if packets[TCP].dport == 80 or packets[TCP].sport == 80:
                    http_payload+=str(packets[TCP].payload)
            except:
                pass

        header=get_http_header(http_payload)

        if header is None:
            continue

        image,image_type=extract_image(header,http_payload)

        if image is not None and image_type is not None:
            carved_images+=1
            file_name="%s-%d.%s" % (pcap_file,carved_images,image_type)
            fd=open("%s/%s"%(pictures_directory,file_name),"wb")

            fd.write(image)
            fd.close()

            try:
                result = face_detect("%s/%s" % (pictures_directory,file_name),file_name)

                if result is True:
                    faces_detect+=1
            except:
                pass

    return carved_images,faces_detect




carved_images,faces_detected=http_assemble(pcap_file)

print "Extracted: %d images" % carved_images
print "Detected: %d faces" % faces_detected