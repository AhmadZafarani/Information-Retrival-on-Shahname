# Ferdosi1401-2_21

گزارش کار

to run the project, download this three files from links below and place them in path : `backend/informationRetrival/logic/`

[classification_pickle.pkl](https://drive.google.com/file/d/1-1c4ODqDi_ssdwOw1ZiEQoJSODVmbboW/view?usp=sharing)

[fasttext_vectors.txt](https://drive.google.com/file/d/1P8yihfE6C8Kmi3VTSfr0CrvzovzL6hBn/view?usp=sharing)

make sure that `docker` and `docker-compose` are installed

run:\
`docker --version`\
resulted in:\
`Docker version 20.10.16, build aa7e414`

also run:\
`docker-compose --version`\
resulted in:\
`docker-compose version 1.29.2, build 5becea4c`

clone project to the mir_project directory, then:
`cd mir_project`\
and now, run:\
`docker-compose up -d`\

if you get permission denied exception, please run above command with sudo \
And wait for the containers... 