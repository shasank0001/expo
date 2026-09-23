---
subject: ml
unit: 1
topic: human-learning
syllabus_ref: CSM3201 Unit-I
status: draft
---
# Human Learning

## Overview

Human learning is a lasting change in knowledge, skills, attitudes, or behaviour that comes from experience, observation, reflection, and practice. It is not simply remembering a fact for one hour: a person can connect new information to old knowledge, try a skill, receive feedback, correct mistakes, and transfer what was learned to a new situation.

Learning matters in the ML syllabus because machine learning is a computational form of learning from examples. Human learning gives useful intuition—students learn from labelled examples, recognise patterns without being told every rule, and improve through feedback—but human and machine learning differ. Humans can reason about context and meaning; a model can only learn the relationships and objective represented in its data and loss function.

## Explanation

### What is human learning?

In psychology and education, learning is commonly described as a relatively permanent change in behaviour or capability produced by experience. The important parts are:

- **Experience:** observation, practice, conversation, reading, success, or failure.
- **Processing:** attention, perception, memory, and reasoning transform the experience.
- **Feedback:** the learner notices whether an action produced the desired result.
- **Retention and transfer:** the skill remains available and can be used in a new context.

A reward is not automatically learning. If a student receives a certificate but cannot later solve a new problem, little useful learning has transferred. A good learning process connects experience to reflection and feedback.

### Major types of human learning

Different textbooks classify learning in several overlapping ways. The following categories are useful for examination purposes.

1. **Rote or mechanical learning.** Facts, vocabulary, formulae, or procedures are memorised through repetition. It is fast for exact recall but weak when the situation changes. Examples include learning multiplication tables or the capitals of countries. Spaced repetition and retrieval practice are more effective than repeatedly rereading.

2. **Meaningful learning.** New information is connected to an existing schema or concept. For example, learning that acceleration is the derivative of velocity is more meaningful when the learner already understands rate of change. Meaningful learning supports transfer and problem solving.

3. **Observational learning.** A learner copies or models behaviour observed in others, including teachers, experts, and peers. Albert Bandura's work is commonly associated with this idea. The learner attends to the model, retains the behaviour, and reproduces it in an appropriate situation. Demonstration, imitation, and social learning are examples.

4. **Experiential or learning by doing.** Skills are learned by acting on the environment. Cycling, programming, nursing, and laboratory work cannot be learned fully from descriptions alone. The cycle is action, observation, feedback, adjustment, and another action. This resembles reinforcement learning, although humans also use conscious goals and prior knowledge.

5. **Cognitive and conceptual learning.** The learner develops understanding of relationships, principles, rules, and mental models. It supports generalisation: the learner can apply a principle to unfamiliar examples. Mathematics, physics, and theory-oriented programming are examples.

6. **Skill and procedural learning.** The learner learns a sequence of actions that produces a result, such as solving a linear equation or using version control. Procedural knowledge is often faster and more reliable when the procedure is explicit and repeated.

7. **Social and emotional learning.** People learn cooperation, empathy, confidence, motivation, and communication. These outcomes matter in teams and in applications of AI, where a technically correct prediction can still fail if people do not trust or use it appropriately.

8. **Self-directed and lifelong learning.** The learner identifies needs, chooses resources, monitors progress, and reflects independently. This is essential in a field such as machine learning because tools, data, and best practices change quickly.

### The learning process

A practical cycle is:

1. **Attention and readiness:** the learner notices a goal and has enough prior knowledge.
2. **Acquisition:** information or a skill is encoded into memory.
3. **Practice and feedback:** the learner performs the task and compares the result with a standard.
4. **Consolidation:** successful strategies are retained and strengthened.
5. **Transfer and adaptation:** the learner uses the idea in a new context.

Cognitive load should be kept appropriate. Too little explanation can produce rote learning; too much complexity at once can overwhelm working memory. Good teaching uses examples, non-examples, gradual practice, retrieval, and feedback.

### Human learning versus machine learning

| Aspect | Human learning | Machine learning |
|---|---|---|
| Input | Sensory experience, language, context | Examples represented as features |
| Goal | Knowledge, skill, understanding, or behaviour | Minimise a specified loss or maximise reward |
| Feedback | Rich, delayed, social, and internal | Numeric loss, labels, or reward |
| Generalisation | Often flexible and concept-based | Depends on data, hypothesis class, and regularisation |
| Errors | Conceptual, motivational, or perceptual | Prediction error encoded in the objective |
| Adaptability | Can reinterpret a situation | Usually learns a fixed mapping or policy |
| Explanation | Can give reasons and contextual caveats | Explanation requires separate techniques |

The comparison is not a claim that machines learn exactly like people. An ML model has no inherent understanding of a doctor's diagnosis or a student's motivation. It estimates a function from data. However, supervised learning imitates the use of examples, unsupervised learning imitates finding structure, and reinforcement learning imitates learning from consequences.

### Example: learning a new subject

A student can learn a linear-regression lesson by memorising the normal equation (rote), understanding the idea of a best-fitting line (meaningful), solving worked problems (procedural), asking peers for corrections (social/observational), and testing the method on new data (transfer). A practical course deliberately uses all these forms. A model trained by gradient descent resembles the procedural/experiential part, but it does not automatically acquire the student's conceptual understanding.

## Worked examples

### Example 1: distinguish learning from a temporary change

A cyclist feels nervous before a race, wears a new helmet, and then rides more cautiously. If the cautious behaviour persists only during the race, the change may be temporary rather than learning. If repeated practice improves balance and the cyclist can use the skill in a new route, it is evidence of learning.

### Example 2: observational learning

A child sees a nurse wash hands before every patient contact and later copies the sequence. The child first observes, retains the order, and reproduces it. If the child understands why hand hygiene matters, meaningful learning has also occurred.

### Example 3: transfer

A learner who can solve \(2x+3=7\) using subtraction can usually solve \(5x+1=16\) by applying the same idea. Transfer is weaker if the learner has memorised only the exact worked example.

### Example 4: link to ML

Suppose a learner sees 20 labelled examples of spam and ordinary e-mail. A simple classifier can use the same input–feedback idea, but its “learning” is only an adjustment of parameters. If new spam contains words unlike the training examples, human understanding may transfer better; the model may fail. This is a useful warning about overfitting and distribution shift.

## Key terms & formulas

- **Learning:** a relatively persistent change caused by experience.
- **Knowledge:** information and concepts a person can recall and use.
- **Skill:** the ability to perform a task effectively.
- **Schema:** an organised mental framework for understanding information.
- **Transfer:** applying learned knowledge or skill to a new situation.
- **Feedback:** information used to judge and improve performance.
- **Reinforcement:** a consequence that increases the likelihood of a behaviour.
- **Forgetting curve:** the usual decline in retention without review.
- **Human generalisation:** successful use of a learned principle beyond its training examples.
- **ML analogue:** a learned mapping \(h_{D}(x)\) that depends on the data set \(D\), rather than a universal human understanding.

## Common mistakes

1. **Equating memorisation with complete learning.** Recall is only one part; explain, apply, and transfer the idea.
2. **Treating reward as learning.** A reward can be ignored or misunderstood; useful learning requires processing and feedback.
3. **Confusing imitation with understanding.** A child can copy an action without knowing its reason.
4. **Assuming human learning is always systematic.** Emotion, fatigue, prior beliefs, and culture affect it.
5. **Saying ML understands like a human.** An ML model has no goals, common sense, or causal explanation unless these are explicitly provided.
6. **Ignoring transfer and forgetting.** A lesson that works only on the same example has limited educational value.

## Exam prep

### Likely 2-mark questions

- **Define human learning.** A lasting change in knowledge, skill, attitude, or behaviour resulting from experience and practice.
- **Name two types of human learning.** Rote/memorisation and meaningful/observational learning are valid examples.
- **Why is feedback important?** It helps a learner compare performance with a goal and correct errors.
- **Give one difference between human and machine learning.** Humans can reason with context; a model learns a statistical mapping from supplied data.

### Long-answer prompts

- **Explain major types of human learning with examples.** Define at least four categories, describe the learning process in each, and give one educational or workplace example.
- **Compare human learning and machine learning.** Discuss examples, feedback, objectives, generalisation, errors, and limitations; finish with a concrete situation in which each is useful.
- **How does learning by doing relate to reinforcement learning?** Explain the action–feedback loop and the differences between a human learner and an RL agent.
