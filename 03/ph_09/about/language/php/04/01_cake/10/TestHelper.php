<?php
namespace App\View\Helper;

use Cake\View\Helper;

class TestHelper extends Helper
{
    public function testHelper($title)
    {
        echo "&lt;h2&gt;". $title ."&lt;/h2&gt;";
    }
}