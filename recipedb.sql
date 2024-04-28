CREATE DATABASE IF NOT EXISTS recipedata;
use recipedata;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Appliances;
DROP TABLE IF EXISTS Ingredients;
DROP TABLE IF EXISTS IngredientTypes;
DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS Units;
DROP TABLE IF EXISTS RecipeIngredients;
DROP TABLE IF EXISTS RecipeAppliances;
DROP TABLE IF EXISTS RecipeCategories;

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

CREATE TABLE Units (
  unitID INT NOT NULL AUTO_INCREMENT,
  unitName VARCHAR(50),
  PRIMARY KEY (unitID)
);

CREATE TABLE RecipeIngredients (
	recipeID INT NOT NULL,
    ingreID INT NOT NULL,
    unitID INT,
    quantity INT,
    PRIMARY KEY (recipeID),
    PRIMARY KEY (ingreID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (ingreID) REFERENCES Ingredients(ingreID)
);

CREATE TABLE RecipeAppliances (
	recipeID INT NOT NULL,
    applianceID INT NOT NULL,
    PRIMARY KEY (recipeID),
    PRIMARY KEY (applianceID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (applianceID) REFERENCES Appliances(applianceID)
);

CREATE TABLE RecipeCategories (
	recipeID INT NOT NULL,
    categoryID INT NOT NULL,
    PRIMARY KEY (recipeID),
    PRIMARY KEY (categoryID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID)
);

#Populate DB with default values
INSERT INTO IngredientTypes (ingtypeName) VALUES ('Vegetables & Greens'), ('Fruits'), ('Spices'), ('Dairy & Eggs'), ('Dairy & Meat Substitutes'),
('Meats'), ('Poultry'), ('Herbs & Spices'), ('Seafood'), ('Grain, Nuts, & Baking Products'), ('Fats & Oils');

INSERT INTO Categories (categoryName) VALUES ('Vegetarian'),('Vegan'),('Dinner'),('Mexican'),('Thai'),('Mediterranean'); 

INSERT INTO	Units (unitName) VALUES ('Cup'),('Teaspoon'),('Tablespoon'),('Milliliter'),('Fluid Ounce'),('Pound'),('Ounce');

SELECT * FROM Units;
SELECT * FROM Categories;