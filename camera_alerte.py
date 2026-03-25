import cv2
import requests
import time

detecteur_visage = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
detecteur_yeux = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
derniere_alerte = 0

def envoyer_alerte(type_alerte):
    try:
        requests.post('http://localhost:5000/alerte', json={
            "type": type_alerte,
            "camera": "salle_1"
        })
    except:
        pass

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    visages = detecteur_visage.detectMultiScale(gris, 1.1, 5)

    for (x, y, w, h) in visages:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        region_visage = gris[y:y+h, x:x+w]
        region_couleur = frame[y:y+h, x:x+w]
        yeux = detecteur_yeux.detectMultiScale(region_visage, 1.1, 10)

        for (ex, ey, ew, eh) in yeux:
            cv2.rectangle(region_couleur, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        maintenant = time.time()

        if len(yeux) >= 2:
            cv2.putText(frame, "Normal", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        elif len(yeux) == 1:
            cv2.putText(frame, "SUSPECT", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            if maintenant - derniere_alerte > 5:
                envoyer_alerte("regard_suspect")
                derniere_alerte = maintenant

        else:
            cv2.putText(frame, "ALERTE", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if maintenant - derniere_alerte > 5:
                envoyer_alerte("visage_cache")
                derniere_alerte = maintenant

    cv2.imshow("Anti-triche", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()