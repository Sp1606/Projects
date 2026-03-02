import '../models/question_model.dart';
import 'question_generator.dart';

class QuizData {
  static List<String> categories = [
    'Math',
    'Science',
    'History',
    'Geography',
    'Arts',
    'Technology',
    'Mixed',
    'Daily Challenge'
  ];

  static List<Question> kidsQuestions = [
    ...QuestionGenerator.generateMathQuestions(),
    
    // SCIENCE - Level 1 Pool (5 questions)
    Question(questionText: 'Which animal is known as the King of the Jungle?', options: ['Tiger', 'Lion', 'Elephant', 'Zebra'], correctAnswerIndex: 1, category: 'Science', level: 1, minAge: 4, maxAge: 8),
    Question(questionText: 'What do bees make?', options: ['Milk', 'Honey', 'Juice', 'Water'], correctAnswerIndex: 1, category: 'Science', level: 1, minAge: 4, maxAge: 8),
    Question(questionText: 'Which bird can swim but cannot fly?', options: ['Duck', 'Penguin', 'Eagle', 'Owl'], correctAnswerIndex: 1, category: 'Science', level: 1, minAge: 4, maxAge: 8),
    Question(questionText: 'What is the color of an emerald?', options: ['Red', 'Blue', 'Green', 'Yellow'], correctAnswerIndex: 2, category: 'Science', level: 1, minAge: 4, maxAge: 8),
    Question(questionText: 'How many colors are in a rainbow?', options: ['5', '6', '7', '8'], correctAnswerIndex: 2, category: 'Science', level: 1, minAge: 4, maxAge: 8),
    
    // SCIENCE - Levels 2-25
    Question(questionText: 'How many legs does a spider have?', options: ['6', '8', '10', '4'], correctAnswerIndex: 1, category: 'Science', level: 2, minAge: 4, maxAge: 8),
    Question(questionText: 'Which planet is the closest to the Sun?', options: ['Venus', 'Earth', 'Mercury', 'Mars'], correctAnswerIndex: 2, category: 'Science', level: 3, minAge: 5, maxAge: 10),
    Question(questionText: 'What is the frozen form of water?', options: ['Steam', 'Ice', 'Cloud', 'Rain'], correctAnswerIndex: 1, category: 'Science', level: 4, minAge: 4, maxAge: 8),
    Question(questionText: 'Which gas do plants absorb from the air?', options: ['Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Helium'], correctAnswerIndex: 1, category: 'Science', level: 5, minAge: 7, maxAge: 12),
    Question(questionText: 'What is the hardest natural substance on Earth?', options: ['Gold', 'Iron', 'Diamond', 'Stone'], correctAnswerIndex: 2, category: 'Science', level: 6),
    Question(questionText: 'Which organ pumps blood through your body?', options: ['Lungs', 'Brain', 'Heart', 'Stomach'], correctAnswerIndex: 2, category: 'Science', level: 7),
    Question(questionText: 'What do we call the path Earth takes around the Sun?', options: ['Circle', 'Orbit', 'Track', 'Road'], correctAnswerIndex: 1, category: 'Science', level: 8),
    Question(questionText: 'What is the study of stars called?', options: ['History', 'Biology', 'Astronomy', 'Math'], correctAnswerIndex: 2, category: 'Science', level: 9),
    Question(questionText: 'Which animal is the largest on Earth?', options: ['Elephant', 'Blue Whale', 'Giraffe', 'Shark'], correctAnswerIndex: 1, category: 'Science', level: 10),
    // ... adding more to level 25
    for (int i = 11; i <= 25; i++)
      Question(questionText: 'Science Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Science', level: i),

    // HISTORY - Level 1 Pool (5 questions)
    Question(questionText: 'Which giant animals lived millions of years ago?', options: ['Mammoths', 'Dinosaurs', 'Dragons', 'Giant Sloths'], correctAnswerIndex: 1, category: 'History', level: 1, minAge: 4, maxAge: 10),
    Question(questionText: 'Who was the first President of the USA?', options: ['Washington', 'Lincoln', 'Jefferson', 'Kennedy'], correctAnswerIndex: 0, category: 'History', level: 1, minAge: 6, maxAge: 12),
    Question(questionText: 'What was the name of the ship that hit an iceberg?', options: ['Titanic', 'Santa Maria', 'Mayflower', 'Britannica'], correctAnswerIndex: 0, category: 'History', level: 1, minAge: 6, maxAge: 12),
    Question(questionText: 'In which country were the first Olympic Games held?', options: ['Italy', 'Greece', 'China', 'USA'], correctAnswerIndex: 1, category: 'History', level: 1, minAge: 6, maxAge: 12),
    Question(questionText: 'Who built the Great Pyramids?', options: ['Romans', 'Greeks', 'Egyptians', 'Aztecs'], correctAnswerIndex: 2, category: 'History', level: 1),
    
    // HISTORY - Levels 2-25
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'History Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'History', level: i),

    // GEOGRAPHY - Level 1 Pool (5 questions)
    Question(questionText: 'Which is the largest continent?', options: ['Africa', 'Europe', 'Asia', 'Australia'], correctAnswerIndex: 2, category: 'Geography', level: 1),
    Question(questionText: 'What is the capital of France?', options: ['London', 'Paris', 'Berlin', 'Madrid'], correctAnswerIndex: 1, category: 'Geography', level: 1),
    Question(questionText: 'Which ocean is the largest?', options: ['Atlantic', 'Pacific', 'Indian', 'Arctic'], correctAnswerIndex: 1, category: 'Geography', level: 1),
    Question(questionText: 'Which country is known as the Land of the Rising Sun?', options: ['China', 'Japan', 'Korea', 'Thailand'], correctAnswerIndex: 1, category: 'Geography', level: 1),
    Question(questionText: 'What is the tallest mountain in the world?', options: ['K2', 'Mount Everest', 'Fuji', 'Kilimanjaro'], correctAnswerIndex: 1, category: 'Geography', level: 1),

    // GEOGRAPHY - Levels 2-25
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Geography Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Geography', level: i),

    // ARTS - Level 1 Pool
    for (int i = 0; i < 5; i++)
      Question(questionText: 'Arts Level 1 Variant $i...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Arts', level: 1),
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Arts Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Arts', level: i),

    // TECHNOLOGY - Level 1 Pool
    for (int i = 0; i < 5; i++)
      Question(questionText: 'Technology Level 1 Variant $i...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Technology', level: 1),
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Technology Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Technology', level: i),

    // GEOGRAPHY
    Question(questionText: 'Which is the largest continent?', options: ['Africa', 'Europe', 'Asia', 'South America'], correctAnswerIndex: 2, category: 'Geography', level: 1, minAge: 5, maxAge: 12),
    Question(questionText: 'Which ocean is the largest?', options: ['Atlantic', 'Indian', 'Arctic', 'Pacific'], correctAnswerIndex: 3, category: 'Geography', level: 2, minAge: 6, maxAge: 12),
    Question(questionText: 'What is the capital of France?', options: ['London', 'Berlin', 'Paris', 'Madrid'], correctAnswerIndex: 2, category: 'Geography', level: 3, minAge: 6, maxAge: 12),
    Question(questionText: 'Which country has the most people?', options: ['India', 'China', 'USA', 'Russia'], correctAnswerIndex: 1, category: 'Geography', level: 4, minAge: 7, maxAge: 14),
    Question(questionText: 'Which desert is the largest hot desert in the world?', options: ['Gobi', 'Kalahari', 'Sahara', 'Thar'], correctAnswerIndex: 2, category: 'Geography', level: 5, minAge: 8, maxAge: 14),

    // ARTS
    Question(questionText: 'Which color do you get by mixing Red and Blue?', options: ['Green', 'Purple', 'Orange', 'Brown'], correctAnswerIndex: 1, category: 'Arts', level: 1, minAge: 4, maxAge: 10),
    Question(questionText: 'Which instrument has black and white keys?', options: ['Guitar', 'Violin', 'Piano', 'Flute'], correctAnswerIndex: 2, category: 'Arts', level: 2, minAge: 4, maxAge: 10),
    Question(questionText: 'Who painted the Mona Lisa?', options: ['Van Gogh', 'Picasso', 'Leonardo da Vinci', 'Michelangelo'], correctAnswerIndex: 2, category: 'Arts', level: 3, minAge: 7, maxAge: 14),
    Question(questionText: 'What is the art of folding paper called?', options: ['Carving', 'Origami', 'Sculpting', 'Knitting'], correctAnswerIndex: 1, category: 'Arts', level: 4, minAge: 6, maxAge: 12),
    Question(questionText: 'Which of these is a primary color?', options: ['Green', 'Orange', 'Yellow', 'Purple'], correctAnswerIndex: 2, category: 'Arts', level: 5, minAge: 5, maxAge: 10),

    // TECHNOLOGY
    Question(questionText: 'What do we use to click on things on a computer screen?', options: ['Keyboard', 'Mouse', 'Printer', 'Scanner'], correctAnswerIndex: 1, category: 'Technology', level: 1, minAge: 4, maxAge: 10),
    Question(questionText: 'What is the "brain" of a computer called?', options: ['RAM', 'CPU', 'Hard Drive', 'Monitor'], correctAnswerIndex: 1, category: 'Technology', level: 2, minAge: 8, maxAge: 15),
    Question(questionText: 'Which of these is a popular search engine?', options: ['Facebook', 'Google', 'Netflix', 'Amazon'], correctAnswerIndex: 1, category: 'Technology', level: 3, minAge: 7, maxAge: 15),
    Question(questionText: 'What does "WWW" stand for?', options: ['World Wide Web', 'Wild West Web', 'World Wide Work', 'Web Wide World'], correctAnswerIndex: 0, category: 'Technology', level: 4, minAge: 9, maxAge: 15),
    Question(questionText: 'Which company makes the iPhone?', options: ['Microsoft', 'Google', 'Apple', 'Samsung'], correctAnswerIndex: 2, category: 'Technology', level: 5, minAge: 6, maxAge: 15),
  ];

  static List<Question> parentsQuestions = [
    // SCIENCE - Level 1 Pool (5 questions)
    Question(questionText: 'What is the most abundant gas in Earth\'s atmosphere?', options: ['Oxygen', 'Hydrogen', 'Nitrogen', 'Carbon Dioxide'], correctAnswerIndex: 2, category: 'Science', level: 1),
    Question(questionText: 'What is the speed of light?', options: ['300k km/s', '150k km/s', '1m km/s', '500k km/s'], correctAnswerIndex: 0, category: 'Science', level: 1),
    Question(questionText: 'How many planets are in our solar system?', options: ['7', '8', '9', '10'], correctAnswerIndex: 1, category: 'Science', level: 1),
    Question(questionText: 'Which element has the atomic number 1?', options: ['Oxygen', 'Helium', 'Hydrogen', 'Carbon'], correctAnswerIndex: 2, category: 'Science', level: 1),
    Question(questionText: 'What is the main component of the Sun?', options: ['Helium', 'Oxygen', 'Hydrogen', 'Nitrogen'], correctAnswerIndex: 2, category: 'Science', level: 1),
    
    // Science Levels 2-25
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Science Level $i Question (Advanced)...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Science', level: i),

    // HISTORY - Level 1 Pool
    for (int i = 0; i < 5; i++)
      Question(questionText: 'History Level 1 Advanced Variant $i...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'History', level: 1),
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'History Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'History', level: i),

    // GEOGRAPHY - Level 1 Pool
    for (int i = 0; i < 5; i++)
      Question(questionText: 'Geography Level 1 Advanced Variant $i...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Geography', level: 1),
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Geography Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Geography', level: i),

    // ARTS - Level 1 Pool
    for (int i = 0; i < 5; i++)
      Question(questionText: 'Arts Level 1 Advanced Variant $i...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Arts', level: 1),
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Arts Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Arts', level: i),

    // TECHNOLOGY - Level 1 Pool
    for (int i = 0; i < 5; i++)
      Question(questionText: 'Technology Level 1 Advanced Variant $i...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Technology', level: 1),
    for (int i = 2; i <= 25; i++)
      Question(questionText: 'Technology Level $i Question...', options: ['A', 'B', 'C', 'D'], correctAnswerIndex: 0, category: 'Technology', level: i),
  ];

  static List<Question> getFilteredQuestions({
    required String category,
    required bool forKids,
    required int level,
    required int age,
    bool isDaily = false,
  }) {
    final all = forKids ? kidsQuestions : parentsQuestions;
    
    var filtered = all.where((q) {
      bool catMatch = category == 'Mixed' || category == 'Daily Challenge' || q.category == category;
      bool levelMatch = q.level == level;
      bool ageMatch = !forKids || (age >= q.minAge && age <= q.maxAge);
      return catMatch && levelMatch && ageMatch;
    }).toList();

    // Fallback: If age filtering removed everything, try just matching category and level
    if (filtered.isEmpty) {
      filtered = all.where((q) {
        bool catMatch = category == 'Mixed' || category == 'Daily Challenge' || q.category == category;
        bool levelMatch = q.level == level;
        return catMatch && levelMatch;
      }).toList();
    }
    
    // Final fallback: just match category if level is also missing
    if (filtered.isEmpty) {
      filtered = all.where((q) => category == 'Mixed' || category == 'Daily Challenge' || q.category == category).toList();
    }

    // Level 1 logic
    if (level == 1 && filtered.isNotEmpty) {
      filtered.shuffle();
      return [filtered.first];
    }

    // Default: return 1 question for any level
    if (filtered.isNotEmpty) {
      return [filtered.first];
    }

    if (isDaily) {
      filtered.shuffle();
      return filtered.take(1).toList();
    }

    return filtered;
  }
}