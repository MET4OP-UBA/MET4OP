# Evolución de los Sistemas de Bases de Datos

Los sistemas de información existen desde las primeras civilizaciones.
Los datos se recopilaban, se estructuraban, se centralizaban y se almacenaban convenientemente.
El objetivo **inmediato** de este proceso era poder recuperar estos mismos datos u otros datos derivados de ellos en cualquier momento, sin necesidad de volverlos a recopilar, paso que solía ser el más costoso o incluso *irrepetible*.
El objetivo **posterior** de un sistema de información es proporcionar a los usuarios información fidedigna sobre el dominio que representaban, con el objetivo de tomar decisiones y realizar acciones más pertinentes que las que se realizarían sin dicha información.

Llamamos base de datos a una colección de datos recopilados y estructurados existente durante un periodo de tiempo.

## Funciones básicas de un sistema de gestión de base de datos

1. Permitir a los usuarios crear nuevas bases de datos y especificar su estructura, utilizando un lenguaje o interfaz especializado, llamado lenguaje o interfaz de definición de datos.

2. Dar a los usuarios la posibilidad de consultar los datos (es decir, recuperarlos parcial o totalmente) y modificarlos, utilizando un lenguaje o interfaz apropiado, generalmente llamado lenguaje de consulta o lenguaje de manipulación de datos.

3. Permitir el almacenamiento de grandes cantidades de datos durante un largo periodo de tiempo, manteniéndolos seguros de accidentes o uso no autorizado y permitiendo un acceso eficiente a los datos para consultas y modificaciones.

4. Controlar el acceso a los datos de muchos usuarios a la vez, impidiendo que las acciones de un usuario pueda afectar a las acciones de otro sobre datos diferentes y que el acceso simultáneo no corrompa los datos.

## Principales características de las bases de datos

1. Independencia lógica y física de los datos.
2. Control centralizado de los datos. 
3. Integridad de los datos. 
4. Minimización de redundancias.
5. Independencias de los datos y las aplicaciones.
6. Acceso concurrente a los datos.

### 1-Independencia lógica y física de los datos

El hardware de almacenamiento y las técnicas físicas de almacenamiento podrán ser modificados sin obligar a la modificación de los programas de aplicación.
Podrán agregarse nuevos ítems de datos, o expandirse la estructura lógica general, sin que sea necesario reescribir los programas de aplicación existentes, solo se modificara la aplicación que los utiliza.

### 2-Control centralizado de los datos

Brinda la posibilidad de control centralizado sobre los recursos de información de una empresa entera u organización. Antiguamente cada aplicación tiene sus propios archivos privados. La función fundamental de un Administrador de Bases de Datos (DBA) es garantizar la seguridad de los datos; los mismos datos son reconocidos como un patrimonio de las organizaciones las cuales requieren una responsabilidad centralizada.

### 3-Integridad de los datos

Garantizar que los datos de la base de datos sean exactos. El control centralizado de la base de datos ayuda a evitar la inconsistencia de los datos, por el mismo hecho de encontrarse en un solo lugar y mediante medidas de seguridad, restricciones y controles para evitar inconsistencias.

### 4-Minimización de redundancias

Como distintas aplicaciones se conectan a la base de datos, no hace falta tanta repetición de datos.

### 5-Independencias de los datos y las aplicaciones

Podemos quitar un programa que se conecta a la base y cambiarlo por otro sin tener que modificar la base. Lo mismo a la inversa podemos cambiar la base de datos y debería ser transparente para los programas que se conectan a ella.

### 6-Acceso concurrente a los datos

Diferentes usuarios pueden acceder simultáneamente a la base mediante técnicas de bloqueo o cerrado de datos accedidos.

## Componentes de un sistema de base de datos

**Hardware**.Máquinas en las que se almacenan las bases de datos.Incorporan unidades de almacenamiento masivo para este fin.
**Software**. Es el sistema gestor de bases de datos. El encargado de administrar las bases de datos.
**Datos**. Incluyen los datos que se necesitan almacenar y los metadatos que son datos que sirven para describir lo que se almacena en la base de datos.
**Usuarios**. Personas que manipulan los datos del sistema. Hay diferentes categorías según sus funciones y según su grado de uso.

## Tipos de base de datos

- Bases de datos jerárquicas
- Base de datos de red
- Bases de datos relacionales
- Bases de datos no relacionales
- Bases de datos multidimensionales
- Bases de datos orientadas a objetos

### Bases de datos jerárquicas

Éstas son bases de datos que, como su nombre indica, almacenan su información en una estructura jerárquica. En este modelo los datos se organizan en una forma similar a un árbol (visto al revés), en donde un nodo padre de información puede tener varios hijos. El nodo que no tiene padres es llamado raíz, y a los nodos que no tienen hijos se los conoce como hojas.
Las bases de datos jerárquicas son especialmente útiles en el caso de aplicaciones que manejan un gran volumen de información y datos muy compartidos permitiendo crear estructuras estables y de gran rendimiento. Una de las principales limitaciones de este modelo es su incapacidad de representar eficientemente la redundancia de datos.

![image.png](attachment:image.png)

### Bases de datos de red

Éste es un modelo ligeramente distinto del jerárquico; su diferencia fundamental es la modificación del concepto de nodo: se permite que un mismo nodo tenga varios padres (posibilidad no permitida en el modelo jerárquico). Fue una gran mejora con respecto al modelo jerárquico, ya que ofrecía una solución eficiente al problema de redundancia de datos; pero, aun así, la dificultad que significa administrar la información en una base de datos de red ha significado que sea un modelo utilizado en su mayoría por programadores más que por usuarios finales.

![image.png](attachment:image.png)

### Base de datos relacional

Una base de datos relacional es una base de datos que cumple con el modelo relacional, el cual es el modelo más utilizado en la actualidad para implementar bases de datos ya planificadas. Permiten establecer interconexiones (relaciones) entre los datos (que están guardados en tablas), y a través de dichas conexiones relacionar los datos de ambas tablas, de ahí proviene su nombre: “Modelo Relacional”.

#### Características

1.Se compone de varias tablas o relaciones.

2.No pueden existir dos tablas con el mismo nombre ni registro.

3.Cada tabla es a su vez un conjunto de registros (filas y columnas).

4.La relación entre una tabla padre y un hijo se lleva a cabo por medio de las claves primarias y ajenas (o foráneas).

5.Las claves primarias son la clave principal de un registro dentro de una tabla y éstas deben cumplir con la integridad de datos.

6.Las claves ajenas se colocan en la tabla hija, contienen el mismo valor que la clave primaria del registro padre; por medio de éstas se hacen las relaciones.

![image.png](attachment:image.png)

### Base de datos no relacional

Utilizan una variedad de modelos de datos para acceder y administrar datos. Estos tipos de bases de datos están optimizados específicamente para aplicaciones que requieren grandes volúmenes de datos, baja latencia y modelos de datos flexibles, lo que se logra mediante la flexibilización de algunas de las restricciones de coherencia de datos en otras bases de datos.

#### Características

1.Flexibilidad: las bases de datos NoSQL generalmente ofrecen esquemas flexibles que permiten un desarrollo más rápido y más iterativo. El modelo de datos flexible hace que las bases de datos NoSQL sean ideales para datos semiestructurados y no estructurados.

2.Escalabilidad: las bases de datos NoSQL generalmente están diseñadas para escalar usando clústeres distribuidos de hardware en lugar de escalar añadiendo servidores caros y sólidos. Algunos proveedores de la nube manejan estas operaciones en segundo plano, como un servicio completamente administrado.

3.Alto rendimiento: la base de datos NoSQL está optimizada para modelos de datos específicos y patrones de acceso que permiten un mayor rendimiento que el intento de lograr una funcionalidad similar con bases de datos relacionales.

4.Altamente funcional: las bases de datos NoSQL proporcionan API altamente funcionales y tipos de datos que están diseñados específicamente para cada uno de sus respectivos modelos de datos.

![image.png](attachment:image.png)

### Bases de datos multidimensionales

Visualización de los datos mediante un cubo. La vista de los datos como un cubo es una extensión natural de como la mayoría de los usuarios interactúan con los datos. Ellos ven a un problema en términos de un cierto número de componentes (dimensiones) tales como productos, tiempo, regiones, fabricantes, o artículos.
Los usuarios desean poder analizar un conjunto de números usando cualquier par de estos componentes, como así también poder intercambiarlos para lograr distintas vistas.

![image.png](attachment:image.png)

### Bases de datos orientadas a objetos

La información se representa mediante objetos como los presentes en la programación orientada a objetos. Las bases de datos orientadas a objetos se diseñan para trabajar bien en conjunción con lenguajes de programación orientados a objetos. Dichos objetos se extienden en los lenguajes como datos persistentes de forma transparente, control de concurrencia, recuperación de datos, consultas asociativas y otras capacidades.

![image.png](attachment:image.png)

## Sistema gestor de base de datos (SGBD)

Un sistema gestor de bases de datos o SGBD (aunque se suele utilizar más a menudo las siglas DBMS procedentes del inglés, Data Base Management System) es el software que permite a los usuarios procesar, describir, administrar y recuperar los datos almacenados en una base de datos. En estos Sistemas se proporciona un conjunto coordinado de programas, procedimientos y lenguajes que permiten a los distintos usuarios realizar sus tareas habituales con los datos, garantizando además la seguridad de los mismos.

### Herramientas proporcionadas

- Herramientas para la creación y especificación de los datos. Así como la estructura de la base de datos.
- Herramientas para administrar y crear la estructura física requerida en las unidades de almacenamiento.
- Herramientas para la manipulación de los datos de las bases de datos, para añadir, modificar, suprimir o consultar datos.
- Herramientas de recuperación en caso de desastre.
- Herramientas para la creación de copias de seguridad.
- Herramientas para la gestión de la comunicación de la base de datos.
- Herramientas para la creación de aplicaciones que utilicen esquemas externos de los datos.
- Herramientas de instalación de la base de datos
- Herramientas para la exportación e importación de datos

## Características deseables en un SGBD

1. Control de redundancia. 
2. Restricción de accesos no autorizados. 
3. Almacenamiento de objetos y estructuras de datos de programas.
4. Inferencias en la BD mediante reglas de deducción. 
5. Suministro múltiple de interfaces con los usuarios. 
6. Recuperación de vínculos complejos entre los datos. 
7. Cumplimiento de las restricciones de integridad. 
8. Respaldo y recuperación.

### Funciones de SGBD

### Función de descripción o de definición
Permite al diseñador de la base de datos crear las estructuras apropiadas para integrar adecuadamente los datos. Este función es la que permite definir las tres estructuras de la base de datos (relacionadas con sus tres esquemas).
- Estructura interna
- Estructura conceptual
- Estructura externa

### Función de manipulación
Permite modificar y utilizar los datos de la base de datos. Se realiza mediante el lenguaje de modificación de datos o DML.Mediante ese lenguaje se puede:
- Añadir datos
- Eliminar datos
- Modificar datos
- Buscar datos

### Función de control
Mediante esta función los administradores poseen mecanismos para proteger las visiones de los datos permitidas a cada usuario, además de proporcionar elementos de creación y modificación de esos usuarios.

## Modelo de datos

La finalidad de un modelo es la de simbolizar una parte del mundo real de forma que sea más fácilmente manipulable. En definitiva es un esquema mental (conceptual) en el que se intentan reproducir las características de una realidad específica. En el caso de los modelos de datos, lo que intentan reproducir es una información real que deseamos almacenar en un sistema informático.
Se denomina esquema a una descripción específica en términos de un modelo de datos. El conjunto de datos representados por el esquema forma la base de datos.

## Diferencias entre el diseño lógico y conceptual.
El modelo conceptual es independiente del Diseño de Base de Datos que se vaya a utilizar. El lógico depende de un tipo de SGBD en particular. El modelo lógico está más cerca del modelo físico, el que utiliza internamente la maquina. El modelo conceptual es el más cercano al usuario, el lógico es el encargado de establecer el paso entre el modelo conceptual y el modelo físico del sistema.

## Modelos conceptuales
1. Modelo de entidad-relación. 
2. Modelo orientado a objetos. 
3. Modelo de datos semántico.
4. Modelo de datos funcional.

### Modelo de entidad-relación
Está basado en una percepción del mundo real que consta de una colección de objetos básicos, llamados entidades, y de relaciones entre estos objetos.
- Una entidad es una «cosa» u «objeto» en el mundo real que es distinguible de otros objetos.
- Los atributos describen propiedades que posee cada miembro de un conjunto de entidades.
- Una relación es una asociación entre varias entidades.

![image.png](attachment:image.png)

Elementos del modelo
• Entidad
• Relación
• Atributo
• Dominio

### Entidad

Se trata de cualquier objeto u elemento (real o abstracto) acerca del cual se pueda almacenar información en la base de datos. Ejemplos de entidades son Pedro, la factura número 32456, el coche patente URS698. Una entidad no es un propiedad concreta sino un objeto que puede poseer múltiples propiedades (atributos).

Las entidades que poseen las mismas propiedades forman conjuntos de entidades. Ejemplos de conjuntos de entidades son los conjuntos: personas, facturas, automóviles
En la actualidad se suele llamar entidad a lo que anteriormente se ha definido como conjunto de entidades. De este modo hablaríamos de la entidad PERSONAS. Mientras que cada persona en concreto sería una ocurrencia o un ejemplar de la entidad persona

![image.png](attachment:image.png)

### Representación gráfica de las entidades

![image.png](attachment:image.png)

### Relaciones

Representan asociaciones entre entidades. Es el elemento del modelo que permite relacionar en sí los datos del modelo.

## Representación gráfica

![image.png](attachment:image.png)

### Correspondencia de cardinalidades

Dado un conjunto de relaciones en el que participan dos o más conjuntos de entidades, la correspondencia de cardinalidad indica el número de entidades con las que puede estar relacionada una entidad dada. Dado un conjunto de relaciones binarias y los conjuntos de entidades A y B, la correspondencia de cardinalidades puede ser:

**Uno a Uno**: Una entidad de A se relaciona únicamente con una entidad en B y viceversa.
Ejemplo: Relación uno a uno (1:1) el actor Darin actuó solo en El Secreto de sus ojos y no en Rocky ni en Titanic. Mientras desde la vista película no solo actuo Darin, no Stallone ni Dicaprio. Lo mismo para los otros actores y películas, solo le corresponde un actor por película y una película por actor.

![image.png](attachment:image.png)

**Uno a varios**: Una entidad en A se relaciona con cero o muchas entidades en B. Pero una entidad en B se relaciona con una única entidad en A.
Ejemplo: Relación uno a muchos (1:M) los animales vivíparos son el perro, el caballo y el gato, no es como el ejemplo anterior de actor película. En este caso Reproducción tiene más de un animal. Y a la inversa el caballo es vivíparo y no ovíparo, la relación en este sentido es única.

![image.png](attachment:image.png)

**Varios a Uno**: Una entidad en A se relaciona exclusivamente con una entidad en B. Pero una entidad en B se puede relacionar con 0 o muchas entidades en A.

**Varios a Varios**: Una entidad en A se puede relacionar con 0 o muchas entidades en B y viceversa.
Ejemplo: Relación muchos a muchos (M:N) José trabaja en más de un proyecto, en los proyectos 1 y 2, pero no trabaja solo en esos proyecto tiene colaboradores.

![image-2.png](attachment:image-2.png)

### Atributos
Propiedad o característica de una entidad. Una entidad particular es descrita por los valores de sus atributos:
Ejemplo: la entidad película tiene los atributos titulo, género, nacionalidad, año de estreno.
![image.png](attachment:image.png)

### Dominio
- Las distintas propiedades o características de un tipo de entidad o de interrelación toman valores para cada ocurrencia de estos.
- El conjunto de los posibles valores que puede tomar una cierta característica se denomina dominio.
- Para saber si un valor pertenece a un dominio determinado comprendemos que cumple un predicado que este lleva siempre asociado.
Ejemplo: el valor ‘ingles’ se toma del dominio Idiomas y cumple con el predicado de ser uno de los idiomas posibles del conjunto {‘frances’;’ingles’}

## Modelos lógicos 
1. Modelo relacional. 
2. Modelo de red. 
3. Modelo jerárquico.

### Modelo relacional
El modelo relacional para la gestión de una base de datos es un modelo de datos basado en la lógica de predicados y en la teoría de conjuntos. Es el modelo más utilizado en la actualidad para modelar problemas reales y administrar datos dinámicamente.

![image.png](attachment:image.png)

**Objetivos**
- Independencia física. La forma de almacenar los datos, no debe influir en su manipulación lógica. Si la forma de almacenar los datos cambia, los usuarios no tienen siquiera porque percibirlo y seguirán trabajando de la misma forma con la base de datos. Esto permite que los usuarios y usuarias se concentren en qué quieren consultar en la base de datos y no en cómo está realizada la misma.
- Independencia lógica. Las aplicaciones que utilizan la base de datos no deben ser modificadas porque se modifiquen elementos de la base de datos. Es decir, añadir, borrar y suprimir datos no influye en las vistas de los usuarios. De una manera más precisa, gracias a esta independencia el esquema externo de la base de datos es realmente independiente del modelo lógico.
- Flexibilidad. La base de datos ofrece fácilmente distintas vistas en función de los usuarios y aplicaciones.
- Uniformidad. Las estructuras lógicas siempre tienen una única forma conceptual (las tablas).
- Sencillez. Facilidad de manejo (algo cuestionable, pero ciertamente verdadero si comparamos con los sistemas gestores de bases de datos anteriores a este modelo).

El elemento fundamental es lo que se conoce como **relación**, aunque más habitualmente se le llama **tabla** (o también array o matriz)

Las relaciones constan de: **Atributos**. Referido a cada propiedad de los datos que se almacenan en la relación (nombre, dni,...).
**Tuplas**. Referido a cada elemento de la relación. Por ejemplo si una relación almacena personas, una tupla representaría a una persona en concreto.
Puesto que una relación se representa como una tabla; podemos entender que las columnas de la tabla son los atributos y las filas las tuplas.

![image.png](attachment:image.png)

## Tupla
Cada una de las filas de la relación. Se corresponde con la idea clásica de registro. Representa por tanto cada elemento individual de esa relación.
Tiene que cumplir que:
- Cada tupla se debe corresponder con un elemento del mundo real.
- No puede haber dos tuplas iguales (con todos los valores iguales).

## Dominio
Conjunto finito de valores del mismo tipo. A los dominios se les asigna un nombre y así podemos referirnos a ese nombre en más de un atributo.

## Propiedades de las tablas o relaciones
- 1. Cada tabla tiene un nombre distinto. 
- 2. Cada atributo de la tabla toma un solo valor en cada tupla. 
- 3. Cada atributo tiene un nombre distinto en cada tabla (aunque puede coincidir en tablas distintas).
- 4. Cada tupla es única (no hay tuplas duplicadas). 
- 5. El orden de los atributos no importa. 
- 6. El orden de las tuplas no importa.

## Claves

- Clave Candidata: Conjunto de atributos que identifican unívocamente cada tupla de la relación. Es decir columnas cuyos valores no se repiten en ninguna otra tupla de esa tabla. Toda tabla en el modelo relacional debe tener al menos una clave candidata (puede incluso haber más).
- Clave Primaria (PK -Primary Key- ): Clave candidata que se escoge como identificador de las tuplas. Se elige como primaria la candidata que identifique mejor a cada tupla en el contexto de la base de datos. Por ejemplo un campo con el DNI sería clave candidata de una tabla de clientes. Si esa tabla tiene un campo de código de cliente, éste sería mejor candidato (y por lo tanto clave principal) porque es mejor identificador para ese contexto.
- Clave Alternativa: Cualquier clave candidata que no sea primaria.
- Clave externa, ajena o secundaria (FK -Foreing Key-): Son los datos de atributos de una tabla cuyos valores están relacionados con atributos de otra tabla

![image.png](attachment:image.png)
![image-2.png](attachment:image-2.png)
