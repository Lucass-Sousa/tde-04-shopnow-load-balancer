FROM php:8.1-apache
WORKDIR /var/www/html

# Instalar extensões básicas
RUN docker-php-ext-install pdo pdo_mysql

# Expor porta interna
EXPOSE 80

# Apache começa automaticamente
CMD ["apache2-foreground"]
