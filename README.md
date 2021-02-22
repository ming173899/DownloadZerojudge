# DownloadZerojudge

##環境安裝

使用anaconda，就可直接使用資料夾裡的zerojudge.yml安裝環境

> `conda env create -f zerojudge.yml`

然後進入環境

> `conda activate selenium`

必須去修改zerojudge.py裡的第46行，改成妳要下載的課程，此code會將你開設課程裡的隨堂小考，學生答對的程式碼都下載下來

> `driver.get('你開設的課程url') #zerojudge course url 要修改這行`

修改完後存檔就可以直接執行

> `python ./zerojudge.py`
