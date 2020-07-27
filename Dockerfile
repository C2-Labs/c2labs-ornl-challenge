
FROM python:3.8-slim

LABEL "Author"="Jed Thornock"
LABEL "Company"="C2 Labs, Inc."
LABEL "Application Name"="Data-Wookies Ornl Challenge"

# Install the core packages
# RUN apk-get update && \
#   apk-get --no-cache add bash npm nodejs coreutils curl g++ tzdata && \
#   rm -rf /var/cache/apk/*i
RUN apt-get update \
&& apt-get install gcc curl -y \
&& apt-get clean

# Copy the src folder to the work folder
COPY ./data-wookies/ /work/

# Install the Python modules
WORKDIR /work/scripts/
RUN pip install -r requirements.txt

#Install NodeJS and NPM packages
WORKDIR /work/
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs && npm install

#Install Angular Packages
WORKDIR /work/client/
RUN npm install -g @angular/cli@9 && npm install && ng build

WORKDIR /work/

CMD ["node", "server.js"]




