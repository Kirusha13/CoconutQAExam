from datetime import datetime
from db_models.movies import MoviesDBModel
from db_requester.models import AccountTransactionTemplate
from utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
import pytest

class TestOtherApi:
    def test_accounts_transaction_template(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)

        stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(100000)}", balance=1000)
        bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(100000)}", balance=500)
        
        # Добавляем записи в сессию
        db_session.add_all([stan, bob])
        # Фиксируем изменения в базе данных
        db_session.commit()
        
        def transfer_money(session, from_account, to_account, amount): 
        # пример функции выполняющей транзакцию
        # представим что она написана на стороне тестируемого сервиса
        # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account_id: ID счета, с которого списываются деньги.
            :param to_account_id: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            # Получаем счета
            from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
            to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            # Проверяем, что на счете достаточно средств
            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            # Выполняем перевод
            from_account.balance -= amount
            to_account.balance += amount

            # Сохраняем изменения
            session.commit()

        try:
            assert stan.balance == 1000
            assert bob.balance == 500
            
            with pytest.raises(ValueError):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=1200)

            db_session.refresh(stan)
            db_session.refresh(bob)

            assert stan.balance == 1000
            assert bob.balance == 500
            
        finally:
            # Удаляем данные для тестирования из базы
            db_session.delete(stan)
            db_session.delete(bob)
            # Фиксируем изменения в базе данных
            db_session.commit()

    def test_delete_movie(self, super_admin, db_session, db_helper, genre_id, new_movie):
        movie_id = 54
        movie_db = db_helper.get_movie_by_id(movie_id)
        if movie_db is None:
            movie_to_add = MoviesDBModel(
            id=movie_id,
            name=new_movie["name"],
            price=new_movie["price"],
            description=new_movie["description"],
            image_url=new_movie["imageUrl"],
            location=new_movie["location"],
            published=new_movie["published"],
            rating=0.0,
            genre_id=genre_id,
            created_at=datetime.now(),
            )
            db_session.add(movie_to_add)
            db_session.commit()
        

        delete_response = super_admin.api.movies_api.delete_movie(movie_id=movie_id)
        assert delete_response.status_code == 200
        assert db_helper.get_movie_by_id(movie_id) is None
        get_response = super_admin.api.movies_api.get_movie_by_id(movie_id=movie_id, expected_status=404)