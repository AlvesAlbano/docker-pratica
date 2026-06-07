FROM mcr.microsoft.com/openjdk/jdk:21-ubuntu
VOLUME /tmp
ARG JAVA_OPTS
ENV JAVA_OPTS=$JAVA_OPTS
COPY target/kotlin.grpc-0.0.1-SNAPSHOT.jar kotlin.jar
EXPOSE 8086
# ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -jar kotlin.jar"]
# For Spring-Boot project, use the entrypoint below to reduce Tomcat startup time.
ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -Djava.security.egd=file:/dev/./urandom -jar kotlin.jar"]
