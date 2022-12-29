FROM mcr.microsoft.com/dotnet/sdk:6.0-jammy AS build

RUN mkdir /home/nethermind

RUN git clone https://github.com/fuseio/nethermind.git /home/nethermind

WORKDIR /home/nethermind

RUN dotnet publish src/Nethermind/Nethermind.Runner -r linux-x64 -c release -o out




FROM mcr.microsoft.com/dotnet/aspnet:6.0-jammy

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get -y install libsnappy-dev libc6-dev libc6

RUN ln -s /usr/lib/x86_64-linux-gnu/libdl.so.2 /usr/lib/x86_64-linux-gnu/libdl.so > /dev/null 2>&1

WORKDIR /nethermind

COPY --from=build /home/nethermind/out .

EXPOSE 8545 30303

VOLUME /nethermind/nethermind_db

VOLUME /nethermind/logs

VOLUME /nethermind/keystore

ENTRYPOINT ["./Nethermind.Runner"]

