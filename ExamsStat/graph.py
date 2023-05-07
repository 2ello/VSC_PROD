import matplotlib.pyplot as plt
import sqlite3
from PIL import Image
import datetime
from datetime import datetime  # noqa: F811


def getInfoFromDB(subject, db_file):
    try:
        conn = sqlite3.connect(db_file)
        cu = conn.cursor()
        dbName = subject[:4]
        records = cu.execute(f"""SELECT * from {dbName}StatTable ORDER BY date""").fetchall()  # noqa: E501
        scoreRow = []
        dateRow = []
        for row in records:
            dateRow.append(row[1])
            if row[0] is None:
                scoreRow.append(0)
            else:
                scoreRow.append(row[0])
        conn.commit()
        cu.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
    return scoreRow, dateRow


def resizeImage(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)


def graphPaint(subject, date, score):
    year = datetime.now().year
    dateR = []
    for i in date:
        dateR.append(datetime.strptime(str(i), '%Y%m%d').strftime('%d\n%b'))
    datePlot = []
    scorePlot = []
    for i in zip(dateR, score):
        if i[1]:
            datePlot.append(i[0])
            scorePlot.append(i[1])
        else:
            pass
    plt.scatter(dateR, score, c=score, s=35, vmin=0, vmax=100)
    plt.plot(datePlot, scorePlot)
    plt.minorticks_on()
    plt.xlabel(f'{year}', fontsize=12)
    plt.ylim([2, 100])
    plt.xlim([dateR[0], dateR[-1]])
    plt.grid(which='major')
    plt.grid(which='minor', linestyle=':')
    plt.tight_layout()
    plt.title(f'{subject}', loc='left', fontsize=10)
    plt.savefig(f'{subject}StatGraphPaint.png')
    plt.clf()
    resizeImage(f'{subject}StatGraphPaint.png',f'{subject}StatGraphPaint.png',size=(700, 500))  # noqa: E501

    
def subjectGraph(subject):

    db_file = "ExamsStat\stat.db"
    score = ()
    date = ()
    score, date = getInfoFromDB(subject, db_file)
    graphPaint(subject, date, score)