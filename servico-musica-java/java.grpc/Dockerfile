FROM mcr.microsoft.com/openjdk/jdk:21-ubuntu
VOLUME /tmp
ARG JAVA_OPTS
ENV JAVA_OPTS=$JAVA_OPTS
COPY target/java.grpc-0.0.1-SNAPSHOT.jar java.jar
EXPOSE 8082
# ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -jar java.jar"]
# For Spring-Boot project, use the entrypoint below to reduce Tomcat startup time.
ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -Djava.security.egd=file:/dev/./urandom -jar java.jar"]
