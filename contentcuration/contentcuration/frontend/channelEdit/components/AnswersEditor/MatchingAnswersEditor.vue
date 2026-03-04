<template>
  <div>
    <div class="grey--text mb-3 text--darken-1">
      Matching Pairs
    </div>
    <div>
      <div v-if="!answers || !answers.length" class="card-border-light pa-3">
        Question has no matching pairs
      </div>
      <div
        v-for="(answer, answerIdx) in answers"
        :key="answerIdx"
        class="card-border-light"
      >
        <VCard class="answer editable" flat data-test="answer">
          <VCardText>
            <VLayout align-top>
              <VFlex xs5>
                <div class="grey--text mb-1">Prompt</div>
                <TipTapEditor
                  v-model="answer.prompt"
                  class="editor"
                  mode="edit"
                  :imageProcessor="EditorImageProcessor"
                  @update="updatePromptText($event, answerIdx)"
                />
              </VFlex>
              <VFlex xs1 class="text-xs-center pt-5">
                <v-icon>arrow_forward</v-icon>
              </VFlex>
              <VFlex xs5>
                <div class="grey--text mb-1">Match</div>
                <TipTapEditor
                  v-model="answer.match"
                  class="editor"
                  mode="edit"
                  :imageProcessor="EditorImageProcessor"
                  @update="updateMatchText($event, answerIdx)"
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
      text="New pair"
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

  const updateAnswersOrder = answers => {
    return answers.map((answer, idx) => {
      return {
        ...answer,
        order: idx + 1,
      };
    });
  };

  function generateId() {
    return Math.random().toString(36).substring(2, 10);
  }

  export default {
    name: 'MatchingAnswersEditor',
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
      updatePromptText(newText, answerIdx) {
        const updatedAnswers = [...this.answers];
        updatedAnswers[answerIdx].prompt = newText;
        this.emitUpdate(updatedAnswers);
      },
      updateMatchText(newText, answerIdx) {
        const updatedAnswers = [...this.answers];
        updatedAnswers[answerIdx].match = newText;
        this.emitUpdate(updatedAnswers);
      },
      addNewAnswer() {
        let updatedAnswers = this.answers ? [...this.answers] : [];
        updatedAnswers = updateAnswersOrder(updatedAnswers);
        updatedAnswers.push({
          prompt: '',
          match: '',
          promptId: `prompt_${generateId()}`,
          matchId: `match_${generateId()}`,
          order: updatedAnswers.length + 1,
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
