#include "th06.hpp"
#include "ResultScreen.hpp"

namespace th06
{

#pragma var_order(scoreData, bytesShifted, xorValue, checksum, bytes, remainingData, decryptedFilePointer, fileLen)
ScoreDat *OpenScore(const char *path)
{
    u8 *bytes;
    i32 bytesShifted;
    i32 fileLen;
    Th6k *decryptedFilePointer;
    i32 remainingData;
    u16 checksum;
    u8 xorValue;
    ScoreDat *scoreData;

    scoreData = (ScoreDat *)FileSystem::OpenPath(path, EXTERNAL_FILE);
    if (scoreData == NULL)
    {
    FAILED_TO_READ:
        scoreData = ZUN_ALLOC_TYPE(ScoreDat);
        scoreData->dataOffset = sizeof(ScoreDat);
        scoreData->fileLen = sizeof(ScoreDat);
    }
    else
    {
        if (g_LastFileSize < sizeof(ScoreDat))
        {
            ZUN_FREE(scoreData);
            goto FAILED_TO_READ;
        }

        remainingData = g_LastFileSize - 2;
        checksum = 0;
        xorValue = 0;
        bytesShifted = 0;
        bytes = &scoreData->xorseed[1];

        while (remainingData > 0)
        {
            xorValue += bytes[0];
            // Invert top 3 bits and bottom 5 bits
            xorValue = (xorValue & 0xe0) >> 5 | (xorValue & 0x1f) << 3;
            // xor one byte later with the resulting inverted bits
            bytes[1] ^= xorValue;
            if (bytesShifted >= 2)
            {
                checksum += bytes[1];
            }
            bytes++;
            remainingData--;
            bytesShifted++;
        }
        if (scoreData->csum != checksum)
        {
            ZUN_FREE(scoreData);
            goto FAILED_TO_READ;
        }
        fileLen = scoreData->fileLen;
        decryptedFilePointer = (Th6k *)((u8 *)scoreData + scoreData->dataOffset);
        fileLen -= scoreData->dataOffset;
        while (fileLen > 0)
        {
            if (decryptedFilePointer->magic == TH6K_MAGIC)
                break;

            decryptedFilePointer = (Th6k *)((u8 *)decryptedFilePointer + decryptedFilePointer->th6kLen);
            fileLen = fileLen - decryptedFilePointer->th6kLen;
        }
        if (fileLen <= 0)
        {
            ZUN_FREE(scoreData);
            goto FAILED_TO_READ;
        }
    }
    scoreData->scores = ZUN_ALLOC_TYPE(ScoreListNode);
    scoreData->scores->next = NULL;
    scoreData->scores->data = NULL;
    scoreData->scores->prev = NULL;
    return scoreData;
}

#pragma var_order(highScore, remainingSize, scoreData, dataScore, score)
u32 GetHighScore(ScoreDat *scoreDat, ScoreListNode *node, u32 character, u32 difficulty)
{
    u32 score;
    u32 dataScore;
    i32 remainingSize;
    Hscr *highScore;
    ScoreDat *scoreData;

    scoreData = scoreDat;

    if (node == NULL)
    {
        ResultScreen::FreeAllScores(scoreData->scores);
        scoreData->scores->next = NULL;
        scoreData->scores->data = NULL;
        scoreData->scores->prev = NULL;
    }

    remainingSize = scoreData->fileLen;
    highScore = (Hscr *)((u8 *)scoreData + scoreData->dataOffset);
    remainingSize -= scoreData->dataOffset;

    while (remainingSize > 0)
    {
        if (highScore->base.magic == HSCR_MAGIC && highScore->base.version == TH6K_VERSION &&
            highScore->character == character && highScore->difficulty == difficulty)
        {
            if (node != NULL)
            {
                ResultScreen::LinkScore(node, highScore);
            }
            else
            {
                ResultScreen::LinkScore(scoreData->scores, highScore);
            }
        }

        remainingSize -= highScore->base.th6kLen;
        highScore = (Hscr *)((u8 *)highScore + highScore->base.th6kLen);
    }
    if (scoreData->scores->next != NULL)
    {
        if (scoreData->scores->next->data->score > 1000000)
        {
            dataScore = scoreData->scores->next->data->score;
        }
        else
        {
            dataScore = 1000000;
        }
        score = dataScore;
    }
    else
    {
        score = 1000000;
    }
    return score;
}

#pragma var_order(parsedCatk, cursor, sd)
ZunResult ParseCatk(ScoreDat *scoreDat, Catk *outCatk)
{
    i32 cursor;
    Catk *parsedCatk;
    ScoreDat *sd;
    sd = scoreDat;

    if (outCatk == NULL)
    {
        return ZUN_ERROR;
    }

    parsedCatk = (Catk *)((u8 *)sd + sd->dataOffset);
    cursor = sd->fileLen - sd->dataOffset;
    while (cursor > 0)
    {
        if (parsedCatk->base.magic == CATK_MAGIC && parsedCatk->base.version == TH6K_VERSION)
        {
            if (parsedCatk->idx >= CATK_NUM_CAPTURES)
                break;

            outCatk[parsedCatk->idx] = *parsedCatk;
        }
        cursor -= parsedCatk->base.th6kLen;
        parsedCatk = (Catk *)&parsedCatk->name[parsedCatk->base.th6kLen - 0x18];
    }
    return ZUN_SUCCESS;
}

#pragma var_order(parsedClrd, characterShotType, cursor, difficulty, sd)
ZunResult ParseClrd(ScoreDat *scoreDat, Clrd *outClrd)
{
    i32 cursor;
    Clrd *parsedClrd;
    ScoreDat *sd;
    i32 characterShotType;
    i32 difficulty;
    sd = scoreDat;

    if (outClrd == NULL)
    {
        return ZUN_ERROR;
    }

    for (characterShotType = 0; characterShotType < SHOTTYPE_COUNT; characterShotType++)
    {
        memset(&outClrd[characterShotType], 0, sizeof(Clrd));

        outClrd[characterShotType].base.magic = CLRD_MAGIC;
        outClrd[characterShotType].base.unkLen = sizeof(Clrd);
        outClrd[characterShotType].base.th6kLen = sizeof(Clrd);
        outClrd[characterShotType].base.version = TH6K_VERSION;
        outClrd[characterShotType].characterShotType = characterShotType;

        for (difficulty = 0; difficulty < ARRAY_SIZE_SIGNED(outClrd[0].difficultyClearedWithoutRetries); difficulty++)
        {
            outClrd[characterShotType].difficultyClearedWithRetries[difficulty] = 1;
            outClrd[characterShotType].difficultyClearedWithoutRetries[difficulty] = 1;
        }
    }

    parsedClrd = (Clrd *)((u8 *)sd + sd->dataOffset);
    cursor = sd->fileLen - sd->dataOffset;
    while (cursor > 0)
    {
        if (parsedClrd->base.magic == CLRD_MAGIC && parsedClrd->base.version == TH6K_VERSION)
        {
            if (parsedClrd->characterShotType >= SHOTTYPE_COUNT)
                break;

            outClrd[parsedClrd->characterShotType] = *parsedClrd;
        }
        cursor -= parsedClrd->base.th6kLen;
        parsedClrd = (Clrd *)((i32)&parsedClrd->base + parsedClrd->base.th6kLen);
    }
    return ZUN_SUCCESS;
}

#pragma var_order(pscr, parsedPscr, character, stage, cursor, difficulty, sd)
ZunResult ParsePscr(ScoreDat *scoreDat, Pscr *outClrd)
{
    i32 cursor;
    Pscr *parsedPscr;
    ScoreDat *sd;
    i32 stage;
    i32 character;
    i32 difficulty;
    sd = scoreDat;
    Pscr *pscr;

    if (outClrd == NULL)
    {
        return ZUN_ERROR;
    }

    for (pscr = outClrd, character = 0; character < SHOTTYPE_COUNT; character++)
    {
        for (stage = 0; stage < PSCR_NUM_STAGES; stage++)
        {
            for (difficulty = 0; difficulty < PSCR_NUM_DIFFICULTIES; difficulty++, pscr++)
            {
                memset(pscr, 0, sizeof(Pscr));

                pscr->base.magic = PSCR_MAGIC;
                pscr->base.unkLen = sizeof(Pscr);
                pscr->base.th6kLen = sizeof(Pscr);
                pscr->base.version = 16;
                pscr->character = character;
                pscr->difficulty = difficulty;
                pscr->stage = stage;
            }
        }
    }

    parsedPscr = (Pscr *)((u8 *)sd + sd->dataOffset);
    cursor = sd->fileLen - sd->dataOffset;

    while (cursor > 0)
    {
        if (parsedPscr->base.magic == PSCR_MAGIC && parsedPscr->base.version == TH6K_VERSION)
        {
            pscr = parsedPscr;
            if (pscr->character >= SHOTTYPE_COUNT || pscr->difficulty >= PSCR_NUM_DIFFICULTIES + 1 ||
                pscr->stage >= PSCR_NUM_STAGES + 1)
                break;

            outClrd[pscr->character * 6 * 4 + pscr->stage * 4 + pscr->difficulty] = *pscr;
        }
        cursor -= parsedPscr->base.th6kLen;
        parsedPscr = (Pscr *)((u8 *)parsedPscr + parsedPscr->base.th6kLen);
    }
    return ZUN_SUCCESS;
}

void ReleaseScoreDat(ScoreDat *scoreDat)
{
    ResultScreen::FreeAllScores(scoreDat->scores);
    ZUN_FREE(scoreDat->scores);
    ZUN_FREE(scoreDat);
}

}
