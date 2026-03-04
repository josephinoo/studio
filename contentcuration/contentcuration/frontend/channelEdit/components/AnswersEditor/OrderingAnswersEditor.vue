<template>
  <div>
    <div class="grey--text mb-3 text--darken-1">
      Ordering Steps
    </div>
    <div class="mb-3">
      Add the steps in the correct order from top-to-bottom. The student will be asked to arrange them in this order.
    </div>
    <div>
      <div v-if="!answers || !answers.length" class="card-border-light pa-3">
        Question has no ordering steps
      </div>
      <div
        v-for="(answer, answerIdx) in answers"
        :key="answerIdx"
        class="card-border-light"
      >
        <VCard class="answer editable" flat data-test="answer">
          <VCardText>
            <VLayout align-top>
              <VFlex shrink class="pt-5 pr-3">
                <div class="title">{{ answerIdx + 1 }}.</div>
              </VFlex>
              <VFlex xs10>
                <div class="grey--text mb-1">Step Content</div>
                <TipTapEditor
                  v-model="answer.answer"
                  class="editor"
                  mode="edit"
                  :imageProcessor="EditorImageProcessor"
                  @update="updateAnswerText($event, answerIdx)"
                />
              </VFlex>
              <VSpacer />
              <VFlex shrink>
                <AssessmentItemToolbar
                  :iconActionsConfig="toolbarIconActions"
                  :canMoveUp="!isAnswerFirst(answerIdx)"
                  :canMoveDown="!isAnswerLast(answerIdx)"
                  class="toolbar"
                  analyticsLabel="Answer"
                  data-test="toolbar"
                  @click="onToolbarClick($event, answerIdx)"
                />
              </VFlex>
            </VLayout>
          </VCardText>
        </VCard>
      </div>
    </div>
    <KButton
      text="New step"
      class="ml-0 mt-3"
      data-test="newAnswerBtn"
      @click="addNewAnswer"
    />
  </div>
</template>

<script>
  import AssessmentItemToolbar from '../AssessmentItemToolbar';
  import { AssessmentItemToolbarActions } from '../../constants';
  import { swapElements } from 'shared/utils/helpers';
  import EditorImageProcessor from 'shared/views/TipTapEditor/TipTapEditor/services/imageService';
  import TipTapEditor from 'shared/views/TipTapEditor/TipTapEditor/TipTapEditor.vue';

  function generateId() {
    return Math.random().toString(36).substring(2, 10);
  }

  const updateAnswersOrder = answers => {
    return answers.map((answer, idx) => {
      return {
        ...answer,
        order: idx + 1,
        correctOrder: idx + 1, // Store explicit correct order based on the list
      };
    });
  };

  export default {
    name: 'OrderingAnswersEditor',
    components: {
      AssessmentItemToolbar,
      TipTapEditor,
    },
    model: {
      prop: 'answers',
      event: 'update',
    },
    props: {
      answers: {
        type: Array,
        default: () => [],
      },
    },
    data() {
      return {
        EditorImageProcessor,
        toolbarIconActions: [
          AssessmentItemToolbarActions.MOVE_ITEM_UP,
          AssessmentItemToolbarActions.MOVE_ITEM_DOWN,
          AssessmentItemToolbarActions.DELETE_ITEM,
        ],
      };
    },
    methods: {
      isAnswerFirst(answerIdx) {
        return answerIdx === 0;
      },
      isAnswerLast(answerIdx) {
        return answerIdx === this.answers.length - 1;
      },
      emitUpdate(updatedAnswers) {
        this.$emit('update', updatedAnswers);
      },
      moveAnswerUp(answerIdx) {
        if (this.isAnswerFirst(answerIdx)) {
          return;
        }
        let updatedAnswers = swapElements(this.answers, answerIdx, answerIdx - 1);
        updatedAnswers = updateAnswersOrder(updatedAnswers);
        this.emitUpdate(updatedAnswers);
      },
      moveAnswerDown(answerIdx) {
        if (this.isAnswerLast(answerIdx)) {
          return;
        }
        let updatedAnswers = swapElements(this.answers, answerIdx, answerIdx + 1);
        updatedAnswers = updateAnswersOrder(updatedAnswers);
        this.emitUpdate(updatedAnswers);
      },
      deleteAnswer(answerIdx) {
        let updatedAnswers = JSON.parse(JSON.stringify(this.answers));
        updatedAnswers.splice(answerIdx, 1);
        updatedAnswers = updateAnswersOrder(updatedAnswers);
        this.emitUpdate(updatedAnswers);
      },
      onToolbarClick(action, answerIdx) {
        switch (action) {
          case AssessmentItemToolbarActions.MOVE_ITEM_UP:
            this.moveAnswerUp(answerIdx);
            break;
          case AssessmentItemToolbarActions.MOVE_ITEM_DOWN:
            this.moveAnswerDown(answerIdx);
            break;
          case AssessmentItemToolbarActions.DELETE_ITEM:
            this.deleteAnswer(answerIdx);
            break;
        }
      },
      updateAnswerText(newText, answerIdx) {
        const updatedAnswers = [...this.answers];
        updatedAnswers[answerIdx].answer = newText;
        this.emitUpdate(updatedAnswers);
      },
      addNewAnswer() {
        let updatedAnswers = this.answers ? [...this.answers] : [];
        updatedAnswers = updateAnswersOrder(updatedAnswers);
        updatedAnswers.push({
          answer: '',
          id: `choice_${generateId()}`,
          order: updatedAnswers.length + 1,
          correctOrder: updatedAnswers.length + 1,
        });
        this.emitUpdate(updatedAnswers);
      },
    },
  };
</script>

<style lang="scss" scoped>
  .card-border-light {
    /* stylelint-disable-next-line custom-property-pattern */
    border: 1px solid var(--v-greyBorder-lighten1);

    &:not(:first-child) {
      border-top: 0;
    }
  }

  .answer {
    position: relative;
  }
</style>
