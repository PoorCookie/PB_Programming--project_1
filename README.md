---
aliases: []
tags: 
created_on:: [[2024-12-23 Monday]]
---

# Сбор статистики для оптимизации русских раскладок для слепопечатников
данный проект представляет собой программу для анализа различных клавиатурных раскладок (русских)

- собственно рассматриваемые раскладки:
	- йцукен
	- вызов
	- диктор
	- скоропись

## Лабораторные и как их запустить

### Установка Git
для клонирования репозитория со всеми лабораторными через консоль нужен установленный **Git**:
#### Linux
```
sudo apt install git
```
#### Windows
-  [ссылка на установщик](https://git-scm.com/downloads/win)

### Клонирование репозитория
```
git clone https://github.com/dolbilko/layout_analyzer.git
```
```
cd layout_analyzer
```
#### Лабораторная 1
**подсчёт нагрузки на пальцы (количество кликов)**

![laba_1](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/laba_1.png)

переключение на ветку этой лабораторной:
```
git checkout laba_1
```
запуск:
```
python layout_analyzer.py 1grams-3.txt
```
названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt`
#### Лабораторная 2
**подсчёт штрафов на пальцы**

![laba_2](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/laba_2.png)

переключение на ветку этой лабораторной:
```
git checkout laba_2
```
запуск:
```
python layout_analyzer.py 1grams-3.txt
```
названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt`
#### Лабораторная 3
**подсчёт распределения штрафов между руками**

![laba_3](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/laba_3.png)

переключение на ветку этой лабораторной:
```
git checkout laba_3
```
запуск:
```
python layout_analyzer.py 1grams-3.txt
```
названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt`
#### Лабораторная 4
**подсчёт одноручных сочетаний и удобных одноручных сочетаний (от мизинца к указательному)**
*количество сочетаний выводиться не на каждую руку по отдельности, а суммарное на две руки*

![laba_4](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/laba_4.png)

переключение на ветку этой лабораторной:
```
git checkout laba_4
```
запуск:
```
python layout_analyzer.py 1grams-3.txt 3
```
названий файлов может быть несколько:
- `python layout_analyzer.py 1grams-3.txt voina-i-mir.txt 3`

последний аргумент - цифра (задаёт максимальную длину рассматриваемых комбинаций)
#### Лабораторная 5
**подсчёт одноручных сочетаний и удобных одноручных сочетаний (от мизинца к указательному) на основе массива всех двухбуквенных сочетаний (без повторений) файлов "1grams-3.txt" и "sortchbukw.csv"**
*количество сочетаний выводиться не на каждую руку по отдельности, а суммарное на две руки*

![laba_5](https://raw.githubusercontent.com/dolbilko/layout_analyzer/57a337a8299139a9ac4823742b87f5745e689782/laba_5_icuken.png)
![laba_5](https://raw.githubusercontent.com/dolbilko/layout_analyzer/57a337a8299139a9ac4823742b87f5745e689782/laba_5_vyzov.png)

переключение на ветку этой лабораторной:
```
git checkout laba_5
```
запуск:
```
python layout_analyzer.py
```



## Вывод

Так как раскладки *Скоропись* и *Диктор* оказались очень схожими как по расположению букв так и по результату анализа - рассмотрим различия раскладок *Йцукен* и *Вызов*.
- *Вызов*:
	- явно выигрывает по распределению нагрузки между пальцами
		- но нагрузка на мизинцы наибольшая среди всех раскладок
	- несколько проигрывает в количестве одноручных комбинаций
- *Йцукен*:
	- огромная нагрузка на указательные пальцы > неизбежное отсутствие сбалансированной нагрузки на пальцы
	- преимущество в наборе всех типов комбинаций, кроме удобных трёхбуквенных (проигрывает всем)
В результате можно сделать вывод, что раскладка *Вызов* может стать лучшей заменой *Йцукена*, правда только если несколько повышенная нагрузка на мизинец не будет критичной

## Приложения
### Рассматриваемый паттерн расположения рук
![raspolojenie](https://raw.githubusercontent.com/dolbilko/layout_analyzer/f82681406946a77645dc047cc239ab71e3df586b/raspolojenie.png)
### Рассматриваемые раскладки
#### Йцукен
![icuken](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/icuken.png)

#### Диктор
![diktor](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/diktor.png)

#### Вызов
![vyzov](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/vyzov.png)


#### Скоропись
![skoropis](https://raw.githubusercontent.com/dolbilko/layout_analyzer/3fd934e05cf0e77c6faac4fd5010f64b815c5ce6/skoropis.png)