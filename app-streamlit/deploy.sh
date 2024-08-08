#usr/zsh

export $(cat .env | xargs)

poetry export --format=requirements.txt > requirements.txt --without-hashes

aws ecr create-repository --respository-name $1
q
docker build -t $1 .

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker tag $1:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$1:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$1:latest

if [ "$2" == "update" ]; then 
    aws lambda delete-function --function-name $1
fi

aws lambda create-function  \
--function-name $1  \
--role  arn:aws:iam::$AWS_ACCOUNT_ID:role/lambda-ex \
--code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$1:latest \
--package-type Image \
--architectures  arm64 \
--environment "Variables={DRY=0,AWS_TELEGRAM_SECRET_NAME=telegram-news-bot-secret,REGION=us-east-1,AWS_TELEGRAM_SECRET_TELEGRAM_TOKEN_KEY=telegram-news-bot-token,AWS_TELEGRAM_SECRET_CHAT_ID_KEY=chat-id}" \
--timeout 120

aws lambda create-function-url-config \
    --function-name $1 \
    --auth-type NONE