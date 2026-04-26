<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpressdb');

/** MySQL database username */
define( 'DB_USER', 'wpuser');

/** MySQL database password */
define( 'DB_PASSWORD', 'wppassword');

/** MySQL hostname */
define( 'DB_HOST', 'mysql:3306');

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'ec9c8ffc263e1f90c1b8a481dfa50d7ee2271012');
define( 'SECURE_AUTH_KEY',  'f4745fb4b17755fb6ffd20a0be4fbde2d358aa15');
define( 'LOGGED_IN_KEY',    'f873301e6469cec2d36f773a5e215d414c837edb');
define( 'NONCE_KEY',        '8cc88ae48e20a3f0dddfa56799e88f5cbbad0995');
define( 'AUTH_SALT',        'f8f082f7e1a63a4a9290fdef14023976033025b4');
define( 'SECURE_AUTH_SALT', 'd2664e41d83e924d8885a6465e79d0c50cae85cf');
define( 'LOGGED_IN_SALT',   'fb76d1e9699bdf4c0e157209e13d4026823e6221');
define( 'NONCE_SALT',       '9bae227b60ccaf29c6dbcf2b46f6b420cf044e19');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

// If we're behind a proxy server and using HTTPS, we need to alert WordPress of that fact
// see also http://codex.wordpress.org/Administration_Over_SSL#Using_a_Reverse_Proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
	$_SERVER['HTTPS'] = 'on';
}

// WORDPRESS_CONFIG_EXTRA
define('WP_HOME', 'http://localhost:8080');
define('WP_SITEURL', 'http://localhost:8080');


/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
