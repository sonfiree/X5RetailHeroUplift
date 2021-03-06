from sklearn.base import clone

from models.utils import make_z, calc_uplift


def uplift_fit(model, X_train, treatment_train, target_train):
    """
    Реализация чуть более сложного способа построения uplift-модели.

    Обучаем бинарный классификатор с целевой переменной:
    Z = Y * W + (1 - Y) * (1 - W)
    где Y - target (купил / не купил),
    W - treatment (было воздействие / не было)

    Uplift считаем по формуле (Бабушкин 5:34):
    Predicted Uplift = 2 * P(Z=1) - 1
    """
    z = make_z(treatment_train, target_train)

    model = clone(model)
    model.fit(X_train, z)

    return model


def uplift_predict(model, X_test):
    predict_z = model.predict_proba(X_test)[:, 1]
    uplift = calc_uplift(predict_z)
    return uplift
