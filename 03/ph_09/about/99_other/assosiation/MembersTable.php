<?php
namespace App\Model\Table;

use App/Model/Entity/Member;
use Cake/ORM/Query;
use Cake/ORM/RulesChecker;
use Cake/ORM/Talbe;
use Cake/Validation/Validator;

class MmebersTable extends Table
{
    public function initialize(array $config)
    {
        parent::initialize($config);

        $this->table('members');
        $this->displayField('name');
        $this->primaryKey('id');

        $this->hasMany('Messages', [
            'foreignKey' => 'members_id'
        ]);
    }

    public function validationDefault(Validator $validator)
    {
        $validator
            ->add('id', 'valid', ['rule' => 'numeric'])
            ->allowEmpty('id', 'create');

        $validator
            ->requirePresence('name', 'create')
            ->notEmpty('name');

        $validator
            ->allowEmpty('mail');

        return $validator;
    }
}