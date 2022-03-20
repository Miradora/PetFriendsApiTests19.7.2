from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """" Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


    """Проверяем, выдает ли полный список питомцев"""

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

    """Проверяем, работает ли фильтр my_pets"""
def test_get_all_pets_with_valid_key_filter(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


"""Проверяем, добавляет ли нового питомца с корректными данными"""
def test_add_new_pet_with_valid_data_correct(name='Мурка', animal_type= 'Сиамский кот', age='7',
                                pet_photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""проверяем, добавляется ли питомец с отрицательным возрастом"""
def test_add_new_pet_with_valid_data_age(name='Мурка', animal_type= 'Сиамский кот', age='-7',
                                pet_photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
#Баг : сайт принимает отрицательные значения возраста#


"""проверяем, добавляется ли питомец с не правильным ключом"""
def test_add_new_pet_with_valid_data_age(name='Мурка', animal_type= 'Сиамский кот', age='7',
                                pet_photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key2 = auth_key['key'] + "123"
    status, result = pf.add_new_pet(auth_key2, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


"""проверяем, добавится ли питомец без имени"""
def test_add_new_pet_with_valid_data_foto(name='' , animal_type= 'Сиамский кот', age='7',
                                pet_photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = auth_key['key']
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
#Баг: Сайт принимает питомца без имени#


"""проверяем, добавится ли питомец при вводе в поле "тип животного" некорректных знаков """
def test_add_new_pet_with_valid_data_foto(name='Мурка' , animal_type= '=^-^=', age='7',
                                pet_photo='images/cat.jpg'):
#Бак : поле "тип животного" принимает некорректные значения#

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = auth_key['key']

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

"""проверяем, добавится ли фото в неверном формате"""
def test_add_new_pet_with_valid_data_foto(name='Мурка' , animal_type= 'Сиамский кот', age='7',
                                pet_photo='images/dog.pdf'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = auth_key['key']

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Баг: сайт принимает фото с форматом PDF

"""Проверем удаление питомца"""
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мурка", "Сиамский кот", "0", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мурка", "Сиамский кот", "0", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_petInfo(name='Мурзик', animal_type='cat', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, myPets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(myPets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")
