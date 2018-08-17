<?php

use Cake\ORM\TableRegistry;

class Example
{
    public function initialize()
    {
        parent::initialize();

        // $this->$uses = "Meetings";と書いてもMeetingsテーブルは読み込まれない
        $this->Meetings = TableRegistry::get('Meetings');
    }

    public function add() {
        $meetings = $this->Meeting->find('list');
    }
}
