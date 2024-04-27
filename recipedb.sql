CREATE DATABASE IF NOT EXISTS recipedata;
use recipedata;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Appliances;
DROP TABLE IF EXISTS Ingredients;
DROP TABLE IF EXISTS IngredientTypes;
DROP TABLE IF EXISTS Recipes;

CREATE TABLE Recipes (
	recipeID INT NOT NULL AUTO_INCREMENT,
    recipeName VARCHAR(100) NOT NULL,
    imagePath VARCHAR(300),
    prepTime INT,
    cookTime INT,
    servingSize INT,
    descriptions VARCHAR(1000),
    instructions VARCHAR(3000),
    PRIMARY KEY (recipeID)
);

CREATE TABLE Categories (
	 categoryID INT NOT NULL AUTO_INCREMENT,
     categoryName VARCHAR(50),
     PRIMARY KEY (categoryID)
);

CREATE TABLE Appliances (
	 applianceID INT NOT NULL AUTO_INCREMENT,
     applianceName VARCHAR(50),
     PRIMARY KEY (applianceID)
);

CREATE TABLE IngredientTypes (
	 ingtypeID INT NOT NULL AUTO_INCREMENT,
     ingtypeName VARCHAR(50),
     PRIMARY KEY (ingtypeID)
);
CREATE TABLE Ingredients (
  ingID INT NOT NULL AUTO_INCREMENT,
  ingtypeID INT,
  ingName VARCHAR(50),
  PRIMARY KEY (ingID),
  FOREIGN KEY (ingtypeID) REFERENCES IngredientTypes(ingtypeID)
);

INSERT INTO IngredientTypes (ingtypeName) VALUES ('Vegetables & Greens'), ('Fruits'), ('Spices'), ('Dairy & Eggs'), ('Dairy & Meat Substitutes'),
('Meats'), ('Poultry'), ('Herbs & Spices'), ('Seafood'), ('Grain, Nuts, & Baking Products'), ('Fats & Oils');



