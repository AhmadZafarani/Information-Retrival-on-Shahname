## Search Engine for Shahname:
In this project, we designed a search engine for Shahname (A long epic poem written by the Persian poet Ferdowsi). After preprocessing the text, we used different models such as Fasttext, TF-IDF,Boolean model, transformers, and elastic search. We also learned a language model for Shahname and used the Rocchio algorithm for query expansion. Finally, we compared Shahname character’s importance with PageRank and HITS (hub and authority) algorithms.

## شاهنامه:
شاهنامه اثر حکیم ابوالقاسم فردوسی توسی، حماسه‌ای منظوم، بر حسب دست نوشته‌های موجود دربرگیرنده نزدیک به ۵۰٬۰۰۰ بیت تا نزدیک به ۶۱٬۰۰۰ بیت و یکی از بزرگ‌ ترین و برجسته‌ترین سروده‌های حماسی جهان است که سرایش آن دست‌آورد دست‌ کم سی سال کارِ پیوسته این سخن‌ سرای نامدار ایرانی است.
در این پروژه متد هایی که در کلاس بازیابی اطلاعات به آن پرداخته شد شامل درست کردن بردارهای معنادار، دسته بندی بر اساس اسامی داستان ها، خوشه بندی و لینک بر روی داده ی شاهنامه پیاده سازی شده است و همچنین هر کدام از این متدها با روش های گوناگون مورد اعتبارسنجی قرار گرفته اند. 


<p align="center">
<img src="./backend/shahname.jpg" height="600">
</p>

<div dir="rtl">

<b>گزارش فنی</b>

فایل [readme](./how-to-run.md) توضیحات لازم برای راه اندازی پروژه به کمک docker و docker-compose را دارا میباشد. کد سرور و elasticsearch در container های جداگانه ای قرار دارند.


<b>Backend</b>

.بخش اصلی اپلیکیشن جنگو، بخش Information Retrieval است که دایرکتوری logic همه logic ما برای ۴ روش بازیابی یعنی boolean، tf-idf، fastext، transformers و clustering و classification و elasticsearch را در بر میگیرد
همچنین داده های مورد نیاز مثل داده های کرال شده قبلی شاهنامه و یا مدل train شده clustering و ابزاری برای خواندن و مرتب کردن آنها نیز موجود میباشد.



<b>Elasticsearch</b>

از elasticsearch 7.14.2 به همراه kibana که یک رابط کاربری گرافیکی برای مشاهده و جستجوی داده های elastic است استفاده میکنیم.

elastic port: 9200
<br/>
kibana port: 5601

دیتاست ها رو به صورت csv ساختیم که بیت ها و id در آنها موجود است و از طریق kibana درون elastic ایندکس کردیم.

در فایل elastic.py ابتدا به سرور الستیک کانکت شدیم و سپس کوئری خود را search میکنیم. و به این صورت بیت مورد نظر در index شاهنامه serack میشود و در پاسخ فایل json ای برگردانده میشود که حاوی ابیات جستجو شده است.


<b>Link Analysis: Page Rank</b>


در تحلیل لینک ابتدا اسامی مختلف شاهنامه را استخراج کردیم و نکته مهم این بود که برای تحلیل اهمیت شخصیت های متخلف می بایست اسامی مختلف شخصیت های یکسان را به همدیگر map میکردیم. به عنوان مثال برای رستم اسامی دیگری مثل تهمتن وجود دارد که ما همه آنها را یکسان در نظر گرفتیم تا بتوانیم اهمین شخصیت ها را استخراج کنیم. کاری که انجام دادیم این بود که برای تشکیل ماتریس transition ها برای هر بیتی که اسم یک شخصیت مهم شاهنامه در آن وجود داشت ما ۷ بیت بالاتر و ۷ بیت پایینتر آن بیت را بررسی کردیم و اگر نام شخصیت مهم دیگری در آن ها بود با توجه به فاصله اش تا بیت اصلی بک وزن اهمیت به
transition
بین آن دو شخصیت میدهیم.
برای مثال اگر در بیت فعلی اسم رستم باشد و در یکی از بیت های بالایی یا پایینی اسم سهراب باشد بسته به فاصله این دو بیت یک میزان به یال بین رستم و سهراب اختصاص میدهیم. به این صورت ما ماتریس transition ها برای الگوریتم page rank آماده کردیم و از این الگوریتم برای استخراج شخصیت های مهم استفاده کردیم.

برای نمایش این شخصیت های مهم از کتابخانه networx استفاده کردیم. به این صورت که چون در واقع در نهایت گرافی داریم که هر کدام از راس های آن میزان اهمیتی دارد و هر کدام از یال هایش نشان دهنده درایه های ماتریس transition هستند، و با استفاده از این کتابخانه گرافی رسم میکنیم که در آن پررنگ و کمرنگ بودن راس گراف با اهمیت آن شخص رابطه مستقیم دارد.



<b>Link Analysis: Hub and Authority</b>

برای این قسمت از آنجایی که ماتریس transition ما متقارن است و الگوریتمی که ما انتخاب کرده ایم این ماتریس را به صورت متقارن تشکیل میدهد، پس خروجی آن دقیقا مانند خروجی های pagerank میشود.


<b>Clustering</b>

ابتدا داده های ۴ داستان سیاوش، ۱۲ رخ، اکوان دیو و رستم و اسفندیار زا از شاهنامه استخراج کردیم. سپس بعد از انجام preprocessing به وسیله روش fasttext روی بیت ها embedding انجام دادیم و سپس روی بردارد های خاص با استفاده از روش k-means کلاسترینگ انجام دادیم.
برای ارزشیابی یک مدل از دو روش rss و brand score استفاده کردیم و برای بهبود مدل حالت ها مختلفی را بررسی کردیم. دو حالت اینکه pre processing انجام بدهیم یا نه و دو حالت مختلف fasttext و در مجموع ۴ حالت را بررسی کردیم و از بین آنها بهترین را انتخاب کردیم.

برای پیدا کردن تعداد cluster های بهینه از silhouette score استفاده مردیم و برای k=1,2,..,15 حالت های مختلف clustering را بررسی کردیم و در نهایت بهترین تعداد کلاستری که به آن رسیدیم ۶ بود.
سپس برای آنکه تشخیص دهیم هر کلاستر مربوطه به چه موضوعی است کلمات پر تکرار هر کدام از آنها را استخراج کردیم و سعی کردیم به توجه به آن ها حدس زدیم که هر کلاستر مربوط به چه موضوعی است برای مثال موضوعات جنگی یا عشق و یار.

برای visualize کردن داده ها و نمایش دادن آنها از T-sne استفاده کردیم. به این صورت که داده ها را کاهش بعد دادیم و در دو بعد نمایش دادیم.

<b>Fasttext</b>

ابتدا مدل را روی کل داده های شاهنامه learn کردیم و پیش به ازای هر query ورودی بعد از embed کردن آن، k بیت نزدیک به آن را از نظر فاصله کسینوسی خروجی داده ایم.
</div>


## MRR Results:

 -|bool|fasttext|tfidf|elastic|transformer|bool_expanded|fasttext_expanded|tfidf_expanded|transformer_expanded|elastic_expanded
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |---
query1|0.0143|0.0033|0.0103|0.001|0.0086|0.0191|0.0101|0.0099|0.0116|0.0138
query2|0.0094|0.0044|0.0139|0.001|0.0087|0.0204|0.0096|0.0118|0.0085|0.0139
query3|0.0134|0.0042|0.0321|0.001|0.0168|0.0238|0.0103|0.0146|0.0072|0.0153
query4|0.0146|0.0081|0.0034|0.0009|0.0035|0.0195|0.0084|0.011|0.0085|0.0125
query5|0.0086|0.0085|0.014|0.0009|0.0103|0.0214|0.0115|0.0115|0.0104|0.015
query6|0.0102|0.0036|0.0237|0.0009|0.009|0.0234|0.0132|0.0162|0.0115|0.0149
query7|0.0093|0.0115|0.0166|0.0009|0.0105|0.0213|0.0136|0.0131|0.0088|0.0148
query8|0.0114|0.0042|0.0122|0.0009|0.0084|0.0167|0.0084|0.0104|0.0029|0.0107
query9|0.0086|0.0041|0.0055|0.0009|0.0034|0.017|0.0076|0.0094|0.0028|0.0106
query10|0.0095|0.007|0.0181|0.0009|0.0084|0.0217|0.0145|0.0135|0.0114|0.0154



## Docker:
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

download this three files from links below and place them in path : `backend/informationRetrival/logic/`

[classification_pickle.pkl](https://drive.google.com/file/d/1-1c4ODqDi_ssdwOw1ZiEQoJSODVmbboW/view?usp=sharing)

[fasttext_vectors.txt](https://drive.google.com/file/d/1P8yihfE6C8Kmi3VTSfr0CrvzovzL6hBn/view?usp=sharing)

[all_vec.out](https://drive.google.com/file/d/11KHGgkyaUyBUzGp1zqJkR75K6TdClkPq/view?usp=sharing)

now we are ready to run the project. To achive that, run:

`cd mir_project`\
and now, run:\
`docker-compose up -d`

if you get permission denied exception, please run above command with sudo \
And wait for the containers... 


## Team members:
|First Name|Last Name|Student ID|
|---|---|---|
|Amirhossein|Alimohammadi|97110166|
|Amirmahdi|Hosseinabadi|97110069|
|Helia|Akhtarkavian|98170657|
|Ahmad|Zaferani|97105985|
|Mohammadhossein|Gheisarieh|97106238|
|Alireza|Babazadeh|97101315|
|Parsa|Rostami|96101646|
