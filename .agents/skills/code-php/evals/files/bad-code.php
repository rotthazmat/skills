<?php

namespace App;

use App\Services\Logger;
use App\Models\User;

class UserProcessor
{
    function process($data)
    {
        if ('active' == $data['status']) {
            $info = array(
                'status' => $data['status'],
                'name' => $data['name'],
                'id' => $data['id'],
            );
            return $info;
        }

        return NULL;
    }

    function label($value)
    {
        return 'Item: ' . $value;
    }

}
