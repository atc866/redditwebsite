from django.shortcuts import render
from . import redditfunction
from . import models
def home(request):
    return render(request,"home.html")

def button(request):
    data =request.POST.get('url')
    print(data)
    redditurl=data
    commentlist=redditfunction.getcomments(redditurl)
    redditfunction.createwordcloud(commentlist)
    redditfunction.emotiongraph(commentlist)
    redditfunction.createbargraph(commentlist)
    return render(request,'home.html',{'url':data})

def external(request):
    data=request.POST.get('param')
    print(data)
    redditurl=data
    #print("database info:")
    #print(models.Redditdatabase.objects.values_list('redditlink'))
    #print(list(models.Redditdatabase.objects.filter(redditlink="https://www.reddit.com/r/GlobalOffensive/comments/16bafch/no_one_has_been_criticizing_mr12_much/").values())[1])
    if(redditfunction.checkurl(redditurl)==True):
        databaselist=list(models.Redditdatabase.objects.filter(redditlink=redditurl).values())
        if(models.Redditdatabase.objects.values_list('redditlink') and len(databaselist)!=0):
            print("in database")
            return render(request,'home.html',{'wordcloud':models.Redditdatabase.objects.filter(redditlink=redditurl).values()[0]['wordcloud']
                                               ,'emotiongraph':models.Redditdatabase.objects.filter(redditlink=redditurl).values()[0]['emotiongraph'],
                                               'bargraph':models.Redditdatabase.objects.filter(redditlink=redditurl).values()[0]['bargraph']})
        else:
            commentlist=redditfunction.getcomments(redditurl)
            wordcloud=redditfunction.createwordcloud(commentlist)
            emotiongraph=redditfunction.emotiongraph(commentlist)
            bargraph=redditfunction.createbargraph(commentlist)
            #print(type(wordcloud))
            ins=models.Redditdatabase(redditlink=data,wordcloud=wordcloud,emotiongraph=emotiongraph,bargraph=bargraph)
            ins.save()
            print("data has been written to the database lets fucking go!")
            print(models.Redditdatabase.objects.values('redditlink'))
            return render(request,'home.html',{'wordcloud':wordcloud,'emotiongraph':emotiongraph,'bargraph':bargraph})
    else:
        return render(request,'home.html',{'badurl':"bad url?? idk"})


