tag=`date "+%Y%m%d_%H%M"`
rm -rf app  &&
mkdir app  &&
cp ../app.py app/app.py   &&
cp ../log_obj.py app/log_obj.py  &&
cp -r ../conf  app/conf    &&
mkdir  app/log    &&
cp -r ../template  app/template    &&
cp -r ../tools  app/tools    &&
cp -r ../route  app/route    &&
cp -r ../other  app/other    &&
cp ../requirement.txt app/requirement.txt  &&
docker build -t kangen/kangen:$tag .  &&
rm -rf app



