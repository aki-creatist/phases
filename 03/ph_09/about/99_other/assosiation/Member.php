<?php
namespace App\Model\Entity;

use Cake/ORM/Entity;

class Member extends Entity
{
    protected $_accessible = [
        '*' => true,
        'id' => false,
    ];
}