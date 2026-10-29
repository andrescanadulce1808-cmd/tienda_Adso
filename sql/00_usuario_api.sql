-- Opcional: crear el usuario de la aplicación (ejecutar con cuenta administrativa).
-- Cambie TuClaveSegura por su propia clave y úsela luego en el archivo .env
CREATE USER IF NOT EXISTS 'api_adso'@'localhost' IDENTIFIED BY 'TuClaveSegura';
GRANT SELECT, INSERT, UPDATE, DELETE ON tienda_adso.* TO 'api_adso'@'localhost';
FLUSH PRIVILEGES;
