<?php

ini_set('upload_max_filesize', '1M');
ini_set('post_max_size', '1M');

$UPLOAD_DIR = __DIR__ . '/uploaded_files';

if (isset($_FILES['uploaded_file'])) {
    $uploaded_file = $_FILES['uploaded_file'];

    $uploaded_file_error = $uploaded_file['error'];
    $uploaded_file_name = $uploaded_file['name'];
    $uploaded_file_tmp_name = $uploaded_file['tmp_name'];
    
    if ($uploaded_file_error !== UPLOAD_ERR_OK) {
        http_response_code(400);
        die(
            "Failed to upload file, error code is $uploaded_file_error; " .
            "google 'PHP File Upload Constants' for details."
        );
    }

    if (!file_exists($UPLOAD_DIR)) {
        mkdir($UPLOAD_DIR);
    }

    move_uploaded_file(
        $uploaded_file_tmp_name,
        "$UPLOAD_DIR/$uploaded_file_name",
    );

    die("File '$uploaded_file_name' uploaded successfully.");
}
?>
<!DOCTYPE html>
<html>
<head><title>Upload File</title></head>
<body>
    <h1>Upload a File</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="uploaded_file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
