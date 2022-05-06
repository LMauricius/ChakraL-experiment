// This file is autogenerated. Edit only function bodies!

#include "../autoinclude/chakralSemanticNodesAutogen.h"
#include <ostream>

namespace ChakraL
{
    
    std::string_view SemanticNode_ContextBlock::className() const {
        return "ContextBlock";
    }
    
    void SemanticNode_ContextBlock::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ContextBlock {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "descs: [" << std::endl;
        for (auto& ptr : descs) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ContextBlock::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + descs.size() + 0);
        for (const auto& ptr : descs) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_DescriptionEntry::className() const {
        return "DescriptionEntry";
    }
    
    void SemanticNode_DescriptionEntry::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "DescriptionEntry {" << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_DescriptionEntry::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_TraitAssertion::className() const {
        return "TraitAssertion";
    }
    
    void SemanticNode_TraitAssertion::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "TraitAssertion {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "cond: "; 
        if (cond) cond->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_TraitAssertion::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            cond.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_Statement::className() const {
        return "Statement";
    }
    
    void SemanticNode_Statement::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "Statement {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "exec: "; 
        if (exec) exec->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_Statement::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            exec.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_Definition::className() const {
        return "Definition";
    }
    
    void SemanticNode_Definition::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "Definition {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "id: "; 
        out << WTokenNames[(int)id.type] << ":" << id.line << ":" << id.character << " - " << id.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "val: "; 
        if (val) val->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "block: "; 
        if (block) block->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_Definition::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            val.get(),
            block.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_AssignmentEqual::className() const {
        return "AssignmentEqual";
    }
    
    void SemanticNode_AssignmentEqual::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "AssignmentEqual {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "left: "; 
        if (left) left->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "op: "; 
        if (op) op->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "rights: "; 
        if (rights) rights->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_AssignmentEqual::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            left.get(),
            op.get(),
            rights.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_IfStat::className() const {
        return "IfStat";
    }
    
    void SemanticNode_IfStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "IfStat {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "cond: "; 
        if (cond) cond->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "exec: "; 
        if (exec) exec->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "alt: "; 
        if (alt) alt->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_IfStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            cond.get(),
            exec.get(),
            alt.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_LoopStat::className() const {
        return "LoopStat";
    }
    
    void SemanticNode_LoopStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "LoopStat {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "parts: [" << std::endl;
        for (auto& ptr : parts) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "block: "; 
        if (block) block->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_LoopStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            block.get(),
        };
        ret.reserve(ret.size() + parts.size() + 0);
        for (const auto& ptr : parts) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_LoopStatPart::className() const {
        return "LoopStatPart";
    }
    
    void SemanticNode_LoopStatPart::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "LoopStatPart {" << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_LoopStatPart::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_TimesLoopStatPart::className() const {
        return "TimesLoopStatPart";
    }
    
    void SemanticNode_TimesLoopStatPart::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "TimesLoopStatPart {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "count: "; 
        if (count) count->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_TimesLoopStatPart::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            count.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_ForLoopStatPart::className() const {
        return "ForLoopStatPart";
    }
    
    void SemanticNode_ForLoopStatPart::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ForLoopStatPart {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "id: "; 
        out << WTokenNames[(int)id.type] << ":" << id.line << ":" << id.character << " - " << id.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "iterable: "; 
        if (iterable) iterable->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ForLoopStatPart::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            iterable.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_WhileLoopStatPart::className() const {
        return "WhileLoopStatPart";
    }
    
    void SemanticNode_WhileLoopStatPart::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "WhileLoopStatPart {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "cond: "; 
        if (cond) cond->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_WhileLoopStatPart::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            cond.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_JumpStat::className() const {
        return "JumpStat";
    }
    
    void SemanticNode_JumpStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "JumpStat {" << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_JumpStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_WithStat::className() const {
        return "WithStat";
    }
    
    void SemanticNode_WithStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "WithStat {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "entries: [" << std::endl;
        for (auto& ptr : entries) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "block: "; 
        if (block) block->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_WithStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            block.get(),
        };
        ret.reserve(ret.size() + entries.size() + 0);
        for (const auto& ptr : entries) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_BreakStat::className() const {
        return "BreakStat";
    }
    
    void SemanticNode_BreakStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "BreakStat {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "id: "; 
        out << WTokenNames[(int)id.type] << ":" << id.line << ":" << id.character << " - " << id.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_BreakStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_ContinueStat::className() const {
        return "ContinueStat";
    }
    
    void SemanticNode_ContinueStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ContinueStat {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "id: "; 
        out << WTokenNames[(int)id.type] << ":" << id.line << ":" << id.character << " - " << id.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ContinueStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_ReturnStat::className() const {
        return "ReturnStat";
    }
    
    void SemanticNode_ReturnStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ReturnStat {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "val: "; 
        if (val) val->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ReturnStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            val.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_YieldStat::className() const {
        return "YieldStat";
    }
    
    void SemanticNode_YieldStat::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "YieldStat {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "val: "; 
        if (val) val->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_YieldStat::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            val.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_Expression::className() const {
        return "Expression";
    }
    
    void SemanticNode_Expression::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "Expression {" << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_Expression::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_ExprBinaryL2R::className() const {
        return "ExprBinaryL2R";
    }
    
    void SemanticNode_ExprBinaryL2R::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ExprBinaryL2R {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operands: [" << std::endl;
        for (auto& ptr : operands) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operators: [" << std::endl;
        for (auto& tok : operators) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; out << WTokenNames[(int)tok.type] << ":" << tok.line << ":" << tok.character << " - " << tok.str << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ExprBinaryL2R::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + operands.size() + 0);
        for (const auto& ptr : operands) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_ExprLUnary::className() const {
        return "ExprLUnary";
    }
    
    void SemanticNode_ExprLUnary::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ExprLUnary {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operators: [" << std::endl;
        for (auto& tok : operators) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; out << WTokenNames[(int)tok.type] << ":" << tok.line << ":" << tok.character << " - " << tok.str << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operands: [" << std::endl;
        for (auto& ptr : operands) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ExprLUnary::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + operands.size() + 0);
        for (const auto& ptr : operands) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_ExprRUnary::className() const {
        return "ExprRUnary";
    }
    
    void SemanticNode_ExprRUnary::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ExprRUnary {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operands: [" << std::endl;
        for (auto& ptr : operands) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operators: [" << std::endl;
        for (auto& tok : operators) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; out << WTokenNames[(int)tok.type] << ":" << tok.line << ":" << tok.character << " - " << tok.str << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ExprRUnary::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + operands.size() + 0);
        for (const auto& ptr : operands) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_ExprPrefixFunction::className() const {
        return "ExprPrefixFunction";
    }
    
    void SemanticNode_ExprPrefixFunction::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ExprPrefixFunction {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operands: [" << std::endl;
        for (auto& ptr : operands) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ExprPrefixFunction::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + operands.size() + 0);
        for (const auto& ptr : operands) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_assignmentCheck::className() const {
        return "assignmentCheck";
    }
    
    void SemanticNode_assignmentCheck::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "assignmentCheck {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operands: [" << std::endl;
        for (auto& ptr : operands) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operators: [" << std::endl;
        for (auto& tok : operators) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; out << WTokenNames[(int)tok.type] << ":" << tok.line << ":" << tok.character << " - " << tok.str << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_assignmentCheck::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + operands.size() + 0);
        for (const auto& ptr : operands) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_RangeLiteral::className() const {
        return "RangeLiteral";
    }
    
    void SemanticNode_RangeLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "RangeLiteral {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operands: [" << std::endl;
        for (auto& ptr : operands) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "operators: [" << std::endl;
        for (auto& tok : operators) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; out << WTokenNames[(int)tok.type] << ":" << tok.line << ":" << tok.character << " - " << tok.str << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_RangeLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + operands.size() + 0);
        for (const auto& ptr : operands) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_Identifier::className() const {
        return "Identifier";
    }
    
    void SemanticNode_Identifier::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "Identifier {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "name: "; 
        out << WTokenNames[(int)name.type] << ":" << name.line << ":" << name.character << " - " << name.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_Identifier::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_Literal::className() const {
        return "Literal";
    }
    
    void SemanticNode_Literal::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "Literal {" << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_Literal::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_FunctionLiteral::className() const {
        return "FunctionLiteral";
    }
    
    void SemanticNode_FunctionLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "FunctionLiteral {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "param: "; 
        if (param) param->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "block: "; 
        if (block) block->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_FunctionLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            param.get(),
            block.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_CoroutineLiteral::className() const {
        return "CoroutineLiteral";
    }
    
    void SemanticNode_CoroutineLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "CoroutineLiteral {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "param: "; 
        if (param) param->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "block: "; 
        if (block) block->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_CoroutineLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            param.get(),
            block.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_ContextBlockLiteral::className() const {
        return "ContextBlockLiteral";
    }
    
    void SemanticNode_ContextBlockLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ContextBlockLiteral {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "items: [" << std::endl;
        for (auto& ptr : items) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ContextBlockLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + items.size() + 0);
        for (const auto& ptr : items) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_ValueLiteral::className() const {
        return "ValueLiteral";
    }
    
    void SemanticNode_ValueLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ValueLiteral {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "val: "; 
        out << WTokenNames[(int)val.type] << ":" << val.line << ":" << val.character << " - " << val.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "suf: "; 
        out << WTokenNames[(int)suf.type] << ":" << suf.line << ":" << suf.character << " - " << suf.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ValueLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_ListLiteral::className() const {
        return "ListLiteral";
    }
    
    void SemanticNode_ListLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "ListLiteral {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "items: [" << std::endl;
        for (auto& ptr : items) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_ListLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + items.size() + 0);
        for (const auto& ptr : items) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_DictLiteral::className() const {
        return "DictLiteral";
    }
    
    void SemanticNode_DictLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "DictLiteral {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "items: [" << std::endl;
        for (auto& ptr : items) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_DictLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + items.size() + 0);
        for (const auto& ptr : items) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_SetLiteral::className() const {
        return "SetLiteral";
    }
    
    void SemanticNode_SetLiteral::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "SetLiteral {" << std::endl; 
        
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "items: [" << std::endl;
        for (auto& ptr : items) {for (size_t i = 0; i<tabs+2; i++) out << tabstr; ptr->print(out, tabs+2, tabstr); out << "," << std::endl; }
        {for (size_t i = 0; i<tabs+1; i++) out << tabstr;} out << "]" << std::endl;
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_SetLiteral::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + items.size() + 0);
        for (const auto& ptr : items) {ret.push_back(ptr.get());}
        return ret;
    }
    
    std::string_view SemanticNode_DictEntry::className() const {
        return "DictEntry";
    }
    
    void SemanticNode_DictEntry::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "DictEntry {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "key: "; 
        if (key) key->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "value: "; 
        if (value) value->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_DictEntry::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            key.get(),
            value.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_MemberDecl::className() const {
        return "MemberDecl";
    }
    
    void SemanticNode_MemberDecl::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "MemberDecl {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "member: "; 
        out << WTokenNames[(int)member.type] << ":" << member.line << ":" << member.character << " - " << member.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "trait: "; 
        if (trait) trait->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "value: "; 
        if (value) value->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_MemberDecl::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            trait.get(),
            value.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_WithStatEntry::className() const {
        return "WithStatEntry";
    }
    
    void SemanticNode_WithStatEntry::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "WithStatEntry {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "id: "; 
        out << WTokenNames[(int)id.type] << ":" << id.line << ":" << id.character << " - " << id.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "val: "; 
        if (val) val->print(out, tabs+1, tabstr); else out << "null";
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_WithStatEntry::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
            val.get(),
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
    std::string_view SemanticNode_AssignmentEqualOperator::className() const {
        return "AssignmentEqualOperator";
    }
    
    void SemanticNode_AssignmentEqualOperator::print(std::wostream& out, size_t tabs, const std::wstring& tabstr) const {
        out << "AssignmentEqualOperator {" << std::endl; 
        
        for (size_t i = 0; i<tabs+1; i++) out << tabstr; out << "op: "; 
        out << WTokenNames[(int)op.type] << ":" << op.line << ":" << op.character << " - " << op.str;
        out << std::endl; 
        
        for (size_t i = 0; i<tabs; i++) out << tabstr; out << "}"; 
    }
    
    std::vector<const SemanticNode*> SemanticNode_AssignmentEqualOperator::getSubNodes() const {
        std::vector<const SemanticNode*> ret {
        };
        ret.reserve(ret.size() + 0);
        return ret;
    }
    
}
